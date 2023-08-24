"""Portfolio choice model functions."""
# Portfolio models
# Written by Jose Ignacio Hernandez
# May 2022

# Load required modules
import numpy as np
import pandas as pd
from pyDOE2 import fullfact
from portchoice.utils import _bfgsmin #, numhess
from numdifftools import Hessian
import time

# Portfolio Logit model
class PortLogit:
    """Portfolio logit model class.

    It contains the routines to prepare the data and estimate a portfolio 
    logit model, as well as for the computation of the optimal portfolio.

    Parameters
    ----------
    Y : pd.DataFrame
        A data frame with choices of each alternative for each respondent.
    X : pd.DataFrame, optional
        A data frame with the alternative-specific variables 
        (e.g., attributes), by default None
    Z : pd.DataFrame, optional
        A data frame with the individual-specific variables, by default None
    C : pd.DataFrame, optional
        A data frame with the costs of each individual alternative for each 
        respondent, by default None
    B_min : float, optional
        Minimum expenditure, by default None
    B_max : float, optional
        Resource constraint, by default None
    B_init : float, optional
        Initial level of consumed resources, 
        by default 0
    interactions : list, optional
        List of alternative-interactions. Each element is a list that marks the 
        alternatives that interact, from 0 to J-1, where J is the number of 
        alternatives, by detault None
    base_combinations : np.ndarray, optional
        Array with initial set of combinations. Can be used to discard unfeasible 
        combinations upfront. If no list is provided, PortChoice will construct a 
        set of all possible combinations from a full-factorial design.
    mutually_exclusive : list, optional
        List of mutually-exclusive alternatives. Each element of the list is
        a numpy array of two elements that detail the two mutually-exclusive
        alternatives, by detault None
    """
    # Init function
    def __init__(self, Y: pd.DataFrame, X: pd.DataFrame = None, Z: pd.DataFrame = None, C: pd.DataFrame = None, B_min: float = None, B_max: float = None, B_init: float = 0., interactions: list = None, base_combinations: np.ndarray = None, mutually_exclusive: list = None):

        # Array of choices
        self.Y = Y.to_numpy()
        
        # Get scalars N and J
        self.N = self.Y.shape[0]
        self.J = self.Y.shape[1]

        # Calculate combinations array
        if base_combinations is not None:
            self.combinations = base_combinations
        else:
            self.combinations = fullfact(np.repeat(2,self.J))
        
        # Interactions
        self.interactions = interactions

        # If mutually-exclusive alternatives are defined, then set utility to -inf
        self.mutually_exclusive = mutually_exclusive
        
        if mutually_exclusive is not None:
            
            idx = []

            # Loop across combinations of mutually-exclusive alts
            for e in mutually_exclusive:

                # Find indexes
                e_j = e - 1
                idx.append(np.where((self.combinations[:,e_j[0]]==1) & (self.combinations[:,e_j[1]]==1))[0])

            # Remove mutually-exclusive alternatives
            idx = np.unique(np.concatenate(idx))

            self.combinations = np.delete(self.combinations,idx,axis=0)

        # Define array for alternative-specific covariates and shape K (if present)
        if X is not None:
            self.K = int(X.shape[1]/self.J)
            self.X = X.to_numpy().reshape((self.N,self.J,self.K))
        else:
            self.K = 0
            self.X = None

        # Define array of individual-specific covariates (if present)
        if Z is not None:
            self.M = Z.shape[1]
            self.Z = Z.to_numpy()
        else:
            self.M = 0
            self.Z = None

        # Define array or budget scalar and feasible combinations (if present)
        self.B_init = B_init

        if B_min is not None:
            if isinstance(B_min,float):
                self.B_min = B_min
            else:
                self.B_min = B_min.to_numpy()
        else:
            self.B_min = B_min


        if B_max is not None:
            if isinstance(B_max,float):
                self.B_max = B_max
            else:
                self.B_max = B_max.to_numpy()
        else:
            self.B_max = B_max

        # Define arrays of costs and totalcosts (if present)
        if C is not None:
            self.C = C.to_numpy()
            self.Totalcosts = self.C @ self.combinations.T

            self.Feasible = np.ones(self.Totalcosts.shape).astype(bool)

            if B_min is not None:
                self.Feasible[(self.B_init + self.Totalcosts.T <= self.B_min).T] = False

            if B_max is not None:
                self.Feasible[(self.B_init + self.Totalcosts.T >= self.B_max).T] = False

        else:
            self.C = 0
            self.Totalcosts = 0.
            self.Feasible = np.ones((self.N,self.combinations.shape[0])).astype(bool)

    # Estimate portfolio logit model
    def estimate(self, startv: np.ndarray, asc: np.ndarray, common_asc: list = None, beta_j: np.ndarray = None, delta_0: float = None, hess: bool = True, tol: float = 1e-6, diffeps: float = (np.finfo(float).eps)**(1/3), verbose: bool = True):
        """Estimate portfolio logit model

        It starts the optimisation routine of the portfolio logit model. 
        The user can specify the presence of alternative-specific constants 
        (`asc`), separate parameters for the alternative-specific variables 
        (`beta_j`) and the presence of a parameter that captures the marginal 
        utility of non-spent resources (`delta_0`).

        Parameters
        ----------
        startv : np.ndarray
            Starting values for the maximum-likelihood estimation routine.
        asc : np.ndarray
            An array of length `n_alternatives`, in which each element can
            be either equal to one if the ASC of the corresponding alternative 
            is estimated, and zero otherwise.
        common_asc: list
            List of lists that indicate the alternatives with common ASCs, 
            by detault None
        beta_j : np.ndarray, optional
            An array of dimension `n_alternatives*n_attributes`, in which each 
            element can be either equal to one if the corresponding 
            alternative-specific parameter is estimated, and zero otherwise. 
            If `beta_j = None` and `X` exists then single attribute-specific 
            parameters (i.e., equal across alternatives) are estimated 
            , by default None
        delta_0 : float, optional
            If None and `C` exists, then the parameter of the marginal utility 
            of non-spent resources is estimated. If `delta_0` is a float, then 
            the parameter is fixed to the value of `delta_0`, by default None
        hess : bool, optional
            Whether the finite-difference hessian is estimated at the end of the 
            estimation routine, by default True
        tol : float, optional
            Tolerance of the gradient in the estimation routine, by default 1e-6
        diffeps : float, optionsl
            Step size of the finite-difference methods (i.e., gradient and Hessian), 
            by detault `np.sqrt(np.finfo(float).eps)`
        verbose : bool, optional
            Whether the estimation routine returns information at each iteration. 
            See the documentation of `scipy.optimize.minimize` with method 
            `l-bfgs-b` for more information, by default True

        Returns
        -------
        ll : float
            Log-likelihood function at the optimum
        coef : numpy.ndarray
            Estimated parameters at the optimum
        se : numpy.ndarray
            Standard errors of `coef`. If `hess = False` and `method` is 
            not 'bfgsmin' then `se = 0.`, else if method is 'bfgsmin', 
            it returns the standard errors computed from the Hessian 
            approximation.
        hessian : numpy.ndarray
            Finite-difference Hessian. If `hess = False` and `method` is 
            not 'bfgsmin' then `hessian = 0.`, else if method is 'bfgsmin', 
            it returns the Hessian approximation.
            approximation
        diff_time : float
            Estimation time in seconds.
        """
        # Retrieve parameter specifications and store in object
        self.asc = asc
        self.common_asc = common_asc
        self.beta_j = beta_j
        self.delta_0 = delta_0

        # Set arguments for the estimation routine
        args = (self.J,self.K,self.M,self.Y,self.C,self.B_min,self.B_max,self.X,self.Z,self.combinations,self.interactions,self.Totalcosts,self.Feasible,self.asc,self.common_asc,self.delta_0,self.beta_j)
            
        # Minimise the LL function
        time0 = time.time()

        res = _bfgsmin(PortLogit._llf,startv,tol=tol,verbose=verbose,difftype='forward',diffeps=diffeps,args=args)
        
        # Get/compute outputs
        ll = res['fun']
        self.coef = res['x'].flatten()

        if verbose:
            print('Computing Hessian')

        if hess:
            hessian = Hessian(PortLogit._llf)(self.coef,self.J,self.K,self.M,self.Y,self.C,self.B_min,self.B_max,self.X,self.Z,self.combinations,self.interactions,self.Totalcosts,self.Feasible,self.asc,self.common_asc,self.delta_0,self.beta_j)
            se = np.sqrt(np.diag(np.linalg.inv(hessian))).flatten()
        else:
            hessian = res['hessian']
            se = np.sqrt(np.diag(np.linalg.inv(hessian))).flatten()

        time1 = time.time()
        diff_time = time1-time0

        # Return results
        return ll, self.coef, se, hessian, diff_time

    # Optimal portfolio
    def optimal_portfolio(self,X: pd.Series = None, Z: pd.DataFrame = None, C: pd.Series = None, B_min: float = None, B_max: float = None, B_init: float = 0, sims: int = 1000, column_names: list = None):
        """Compute the optimal portfolio

        Computes the optimal portfolio based on the estimation results 
        (i.e., obtained from `estimate()`) and user-defined variables. 
        The optimal portfolio is computed by computing the expected 
        utility of all possible combinations of alternatives. The 
        expected utility is computed by simulation using `sims` error 
        draws from an Extreme Value (Gumbel) distribution.

        Parameters
        ----------
        X : pd.Series, optional
            Series of alternative-specific variables, by default None
        Z : pd.DataFrame, optional
            Data frame with individual-specific variables, by default None
        C : pd.Series, optional
            Series with individual costs per alternative, by default None
        B_min : float, optional
            Minimum expenditure, by default None
        B_max : float, optional
            Resource constraint, by default None
        B_init : float, optional
            Initial level of consumed resources, 
            by default 0
        sims : int, optional
            Number of Extreme Value random draws, by default 1000
        column_names : list, optional
            List of column names for the optimal portfolio. If no list is 
            provided, then a generic list of column names will be 
            generated, by default None

        Returns
        -------
        portfolio : pd.DataFrame
            Data frame with the optimal portfolio (ranked combinations),
            its expected utility and its total cost (if `C` is not None).
        """
        # Define array for alternative-specific covariates and shape K (if present)
        if X is not None:
            X = X.to_numpy().reshape((1,self.J,self.K))
        else:
            X = None

        # Raise error if optimal portfolio is comptued with individual-specific variables
        if Z is not None:
            raise ValueError('Optimal portfolio with individual-specific variables is not implemented yet')

        # Define arrays of costs and totalcosts (if present)
        if C is not None:
            Totalcosts = (self.combinations * C.to_numpy()).sum(axis=1)[np.newaxis,:]

            Feasible = np.ones(Totalcosts.shape).astype(bool)

            if B_min is not None:
                Feasible[B_init + Totalcosts <= B_min] = False

            if B_max is not None:
                Feasible[B_init + Totalcosts >= B_max] = False

        else:
            Totalcosts = 0.
            Feasible = np.ones((1,self.combinations.shape[0])).astype(bool)

        # Create random Gumbel draws
        e = np.random.gumbel(size=(sims,self.combinations.shape[0]))

        # Get utility of each portfolio
        Vp = _utility(self.coef,self.J,self.K,self.M,None,C,B_min,B_max,X,Z,self.combinations,self.interactions,Totalcosts,Feasible,self.asc,self.common_asc,self.delta_0,self.beta_j,return_chosen=False)

        # Compute utility for each simulation and average
        Up_s = Vp + e
        Up = Up_s.mean(axis=0)

        # Set utility of unfeasible combinations as -inf
        # if B is not None:
        #     Up[~Feasible.flatten()] = -np.inf

        # Sort portfolios and costs by expected utility
        sort_index = np.argsort(Up)[::-1]
        combinations_sorted = self.combinations[sort_index,:]
        EU_sorted = Up[sort_index]

        # If costs are present, add to the frame and drop unfeasible combinations
        if C is not None:
            Totalcosts_sorted = Totalcosts.flatten()[sort_index]

            Totalcosts_sorted = Totalcosts_sorted[EU_sorted != -np.inf]
            combinations_sorted = combinations_sorted[EU_sorted != -np.inf]
            EU_sorted = EU_sorted[EU_sorted != -np.inf]

        # Construct dataframe for output
        if column_names is None:
            column_names = ['Alt_' + str(i+1) for i in range(self.J)]

        portfolio = np.c_[combinations_sorted,EU_sorted]

        if C is not None:
            portfolio = np.c_[portfolio,Totalcosts_sorted]
            portfolio = pd.DataFrame(portfolio,columns = column_names + ['EU','Costs'])
        else: 
            portfolio = pd.DataFrame(portfolio,columns = column_names + ['EU'])
            
        # Return pandas dataframe
        return portfolio

    # Finite-difference Hessian
    def hessian(self, eps: float = (np.finfo(float).eps)**(1/3)):
        hess = Hessian(PortLogit._llf,eps=eps)(self.coef,self.J,self.K,self.Y,self.C,self.B,self.X,self.Z,self.combinations,self.interactions,self.Totalcosts,self.Feasible,self.asc,self.delta_0,self.beta_j)
        return hess

    # Portfolio choice model log-likelihood function
    @staticmethod
    def _llf(pars,J,K,M,Y,C,B_min,B_max,X,Z,combinations,interactions,Totalcosts,Feasible,asc,common_asc,delta_0,beta_j):
                
        # Get utility functions of chosen alternatives and of portfolios
        Vp, Vp_chosen = _utility(pars,J,K,M,Y,C,B_min,B_max,X,Z,combinations,interactions,Totalcosts,Feasible,asc,common_asc,delta_0,beta_j, return_chosen = True)

        # Clip to avoid numerical overflow
        Vp[Vp>700] = 700
        Vp_chosen[Vp_chosen>700] = 700
        
        prob_1 = np.exp(Vp_chosen)
        prob_2 = np.sum(np.exp(Vp),axis=1)

        # Get choice probability
        probs = prob_1/prob_2
        probs[~np.isfinite(probs)] = 1

        # Log-likelihood is the negative of the sum of LN of choice probabilities
        ll = -np.sum(np.log(probs))

        # Return log-likelihood
        return ll

# Portfolio Logit model
class LCPortLogit:
    """Latent class Portfolio logit model class.

    It contains the routines to prepare the data and estimate a latent 
    class portfolio logit model, as well as for the computation of the 
    optimal portfolio.

    Parameters
    ----------
    Y : pd.DataFrame
        A data frame with choices of each alternative for each respondent.    
    lc : int
        Number of latent classes.    
    X : pd.DataFrame, optional
        A data frame with the alternative-specific variables 
        (e.g., attributes), by default None
    Z : pd.DataFrame, optional
        A data frame with the individual-specific variables, by default None
    C : pd.DataFrame, optional
        A data frame with the costs of each individual alternative for each 
        respondent, by default None
    B : float, optional
        Resource constraint, by default None
    base_combinations : np.ndarray, optional
        Array with initial set of combinations. Can be used to discard unfeasible 
        combinations upfront. If no list is provided, PortChoice will construct a 
        set of all possible combinations from a full-factorial design.
    mutually_exclusive : list, optional
        List of mutually-exclusive alternatives. Each element of the list is
        a numpy array of two elements that detail the two mutually-exclusive
        alternatives.
    """
    # Init function
    def __init__(self,Y: pd.DataFrame, lc: int, X: pd.DataFrame = None, Z: pd.DataFrame = None, C: pd.DataFrame = None, B: float = None, B_init: float = 0., base_combinations: np.ndarray = None, mutually_exclusive: list = None):

        # Array of choices
        self.Y = Y.to_numpy()

        # Latent classes
        self.lc = lc

        # Get scalars N and J
        self.N = self.Y.shape[0]
        self.J = self.Y.shape[1]

        # Calculate combinations array
        if base_combinations is not None:
            self.combinations = base_combinations
        else:
            self.combinations = fullfact(np.repeat(2,self.J))

        # Interactions are still not supported
        self.interactions = None

        # If mutually-exclusive alternatives are defined, then set utility to -inf
        self.mutually_exclusive = mutually_exclusive
        
        if mutually_exclusive is not None:
            
            idx = []

            # Loop across combinations of mutually-exclusive alts
            for e in mutually_exclusive:

                # Find indexes
                e_j = e - 1
                idx.append(np.where((self.combinations[:,e_j[0]]==1) & (self.combinations[:,e_j[1]]==1))[0])

            # Remove mutually-exclusive alternatives
            idx = np.unique(np.concatenate(idx))

            self.combinations = np.delete(self.combinations,idx,axis=0)

        # Define array for alternative-specific covariates and shape K (if present)
        if X is not None:
            self.K = int(X.shape[1]/self.J)
            self.X = X.to_numpy().reshape((self.N,self.J,self.K))
        else:
            self.K = 0
            self.X = None

        # Define array of individual-specific covariates (if present)
        if Z is not None:
            self.M = Z.shape[1]
            self.Z = Z.to_numpy()
        else:
            self.M = 0
            self.Z = None

        # Define array or budget scalar and feasible combinations (if present)
        self.B_init = B_init
        if B is not None:
            if isinstance(B,float):
                self.B = B
            else:
                self.B = B.to_numpy()
        else:
            self.B = B

        # Define arrays of costs and totalcosts (if present)
        if C is not None:
            self.C = C.to_numpy()
            self.Totalcosts = self.C @ self.combinations.T
            
            if B is not None:
                self.Feasible = (self.B_init + self.Totalcosts.T <= self.B).T
            else:
                self.Feasible = np.ones(self.Totalcosts.shape)                
        else:
            self.C = 0
            self.Totalcosts = 0.
            self.Feasible = np.ones(self.combinations.shape)  

    # Estimate latent class portfolio logit model
    def estimate(self, startv: np.ndarray, asc: np.ndarray, beta_j: np.ndarray = None, delta_0: float = None, hess: bool = True, tol: float = 1e-6, diffeps: float = (np.finfo(float).eps)**(1/3), verbose: bool = True):
        """Estimate latent class portfolio logit model

        It starts the optimisation routine of the latent class portfolio logit model. 
        The user can specify the presence of alternative-specific constants 
        (`asc`), separate parameters for the alternative-specific variables 
        (`beta_j`) and the presence of a parameter that captures the marginal 
        utility of non-spent resources (`delta_0`).

        Parameters
        ----------
        startv : np.ndarray
            Starting values for the maximum-likelihood estimation routine.
        asc : np.ndarray
            An array of length `n_alternatives`, in which each element can
            be either equal to one if the ASC of the corresponding alternative 
            is estimated, and zero otherwise.
        beta_j : np.ndarray, optional
            An array of dimension `n_alternatives*n_attributes`, in which each 
            element can be either equal to one if the corresponding 
            alternative-specific parameter is estimated, and zero otherwise. 
            If `beta_j = None` and `X` exists then single attribute-specific 
            parameters (i.e., equal across alternatives) are estimated 
            , by default None
        delta_0 : float, optional
            If None and `C` exists, then the parameter of the marginal utility 
            of non-spent resources is estimated. If `delta_0` is a float, then 
            the parameter is fixed to the value of `delta_0`, by default None
        hess : bool, optional
            Whether the finite-difference hessian is estimated at the end of the 
            estimation routine, by default True
        tol : float, optional
            Tolerance of the gradient in the estimation routine, by default 1e-6
        diffeps : float, optionsl
            Step size of the finite-difference methods (i.e., gradient and Hessian), 
            by detault `np.sqrt(np.finfo(float).eps)`
        verbose : bool, optional
            Whether the estimation routine returns information at each iteration. 
            See the documentation of `scipy.optimize.minimize` with method 
            `l-bfgs-b` for more information, by default True

        Returns
        -------
        ll : float
            Log-likelihood function at the optimum
        coef : numpy.ndarray
            Estimated parameters at the optimum
        se : numpy.ndarray
            Standard errors of `coef`. If `hess = False` then `se = 0.`
        hessian : numpy.ndarray
            Finite-difference Hessian. If `hess = False` then `hessian = 0.`
        diff_time : float
            Estimation time in seconds.
        """
        # Retrieve parameter specifications and store in object
        self.asc = asc
        self.beta_j = beta_j
        self.delta_0 = delta_0

        # Set arguments for the estimation routine
        args = (self.J,self.K,self.M,self.Y,self.C,self.B,self.X,self.Z,self.combinations,self.interactions,self.Totalcosts,self.Feasible,self.asc,self.delta_0,self.beta_j,self.lc)
            
        # Minimise the LL function using BFGSmin
        time0 = time.time()
        res = _bfgsmin(LCPortLogit._llf,startv,tol=tol,verbose=verbose,difftype='forward',diffeps=diffeps,args=args)
        
        # Get/compute outputs
        ll = res['fun']
        self.coef = res['x'].flatten()

        if verbose:
            print('Computing Hessian')

        if hess:
            hessian = Hessian(LCPortLogit._llf)(self.coef,self.J,self.K,self.M,self.Y,self.C,self.B,self.X,self.Z,self.combinations,self.interactions,self.Totalcosts,self.Feasible,self.asc,self.delta_0,self.beta_j,self.lc)
            se = np.sqrt(np.diag(np.linalg.inv(hessian))).flatten()
        else:
            hessian = res['hessian']
            se = np.sqrt(np.diag(np.linalg.inv(hessian))).flatten()

        time1 = time.time()
        diff_time = time1-time0

        # Return results
        return ll, self.coef, se, hessian, diff_time

    # Optimal portfolio
    def optimal_portfolio(self,X: pd.Series = None, Z: pd.DataFrame = None, C: pd.Series = None, B: float = None, B_init: float = 0, sims: int = 1000):
        """Compute the optimal portfolio

        Computes the optimal portfolio based on the estimation results 
        (i.e., obtained from `estimate()`) and user-defined variables. 
        The optimal portfolio is computed by computing the expected 
        utility of all possible combinations of alternatives. The 
        expected utility is computed by simulation using `sims` error 
        draws from an Extreme Value (Gumbel) distribution.

        Parameters
        ----------
        X : pd.Series, optional
            Series of alternative-specific variables, by default None
        Z : pd.DataFrame, optional
            Data frame with individual-specific variables, by default None
        C : pd.Series, optional
            Series with individual costs per alternative, by default None
        B : float, optional
            Resource constraint, by default None
        B_init : float, optional
            Initial level of consumed resources, 
            by default 0
        sims : int, optional
            Number of Extreme Value random draws, by default 1000

        Returns
        -------
        portfolio : pd.DataFrame
            Data frame with the optimal portfolio (ranked combinations),
            its expected utility and its total cost (if `C` is not None).
        """
        # Define array for alternative-specific covariates and shape K (if present)
        if X is not None:
            X = X.to_numpy().reshape((1,self.J,self.K))
        else:
            X = None

        # Raise error if optimal portfolio is comptued with individual-specific variables
        if Z is not None:
            raise ValueError('Optimal portfolio with individual-specific variables is not implemented yet')
            
        # Define arrays of costs and totalcosts (if present)
        if C is not None:
            Totalcosts = (self.combinations * C.to_numpy()).sum(axis=1)[np.newaxis,:]
            if B is not None:
                Feasible = B_init + Totalcosts <= B
            else:
                Feasible = np.ones((1,self.combinations.shape[0])).astype(bool)
        else:
            Totalcosts = 0.
            Feasible = np.ones((1,self.combinations.shape[0]))

        # Create random Gumbel draws
        e = np.random.gumbel(size=(sims,self.combinations.shape[0]))

        # Get utility of each portfolio
        Vp = _utility(self.coef,self.J,self.K,None,C,B,X,Z,self.combinations,self.interactions,Totalcosts,Feasible,self.asc,self.delta_0,self.beta_j,return_chosen=False)

        # Compute utility for each simulation and average
        Up_s = Vp + e
        Up = Up_s.mean(axis=0)

        # Set utility of unfeasible combinations as -inf
        if B is not None:
            Up[~Feasible] = -np.inf

        # Sort portfolios and costs by expected utility
        sort_index = np.argsort(Up)[::-1]
        combinations_sorted = self.combinations[sort_index,:]
        EU_sorted = Up[sort_index]

        # If costs are present, add to the frame and drop unfeasible combinations
        if C is not None:
            Totalcosts_sorted = Totalcosts[sort_index]

            Totalcosts_sorted[EU_sorted != -np.inf]
            combinations_sorted = combinations_sorted[EU_sorted != -np.inf]
            EU_sorted = EU_sorted[EU_sorted != -np.inf]

        # Construct dataframe with expected utility
        portfolio_columns = ['Alt_' + str(i+1) for i in range(self.J)]
        portfolio = pd.concat([ pd.DataFrame(combinations_sorted,columns=portfolio_columns),
                                pd.Series(EU_sorted,name='EU')],axis=1)
        
        if C is not None:
            portfolio = pd.concat([portfolio,pd.Series(Totalcosts_sorted,name='Totalcosts')],axis=1)

        # Return pandas dataframe
        return portfolio

    # Finite-difference Hessian
    def hessian(self, eps: float = (np.finfo(float).eps)**(1/3)):
        hess = Hessian(LCPortLogit._llf,eps=eps)(self.coef,self.J,self.K,self.Y,self.C,self.B,self.X,self.Z,self.combinations,self.interactions,self.Totalcosts,self.Feasible,self.asc,self.delta_0,self.beta_j,self.lc)
        return hess

    # Log-likelihood function
    @staticmethod
    def _llf(pars,J,K,Y,C,B,X,Z,combinations,interactions,Totalcosts,Feasible,asc,delta_0,beta_j,lc):
    

        # Set utility parameters in a list
        pars_utility = []
        par_count = 0
        npars = int((len(pars)-(lc-1))/lc) #int(len(pars[:-(lc-1)])/lc)
        for c in range(lc):
            pars_utility.append(pars[par_count:(par_count+npars)])
            par_count += npars

        # Separate class parameters and transform to probabilities (last lc-1 pars are the class membership parameters. First lc par is fixed in zero)
        pars_classes = np.concatenate((0.,pars[par_count:(par_count+lc-1)]),axis=None)
        probs_classes = np.exp(pars_classes)/np.sum(np.exp(pars_classes))

        # Get utility of chosen alternatives and of portfolios per class
        probs_lc = []

        for c in range(lc):
            Vp, Vp_chosen = _utility(pars_utility[c],J,K,Y,C,B,X,Z,combinations,interactions,Totalcosts,Feasible,asc,delta_0,beta_j, return_chosen = True)

            # Clip to avoid numerical overflow
            Vp[Vp>700] = 700
            Vp_chosen[Vp_chosen>700] = 700
        
            prob_1 = np.exp(Vp_chosen)
            prob_2 = np.sum(np.exp(Vp),axis=1)

            # Get choice probability
            probs_c = prob_1/prob_2
            probs_c[~np.isfinite(probs_c)] = 1

            probs_lc.append(probs_c)
        
        probs_lc = np.vstack(probs_lc).T

        # Create unconditional probabilities
        probs = np.sum(probs_classes * probs_lc, axis=1)

        # Log-likelihood is the negative of the sum of LN of choice probabilities
        ll = -np.sum(np.log(probs))

        # Return log-likelihood
        return ll

# Portfolio Kuhn-Tucker (MDCEV) model
class PortKT:
    """Portfolio Kuhn-Tucker (MDCEV) model class.

    It contains the routines to prepare the data and estimate a portfolio 
    Kuhn-Tucker model, also known as the MDCEV-type model. Support for 
    optimal portfolio is still on the works.

    Parameters
    ----------
    Y : pd.DataFrame
        A data frame with choices of each alternative for each respondent.
    C : pd.DataFrame
        A data frame with the costs of each individual alternative for each 
        respondent
    B : float
        Resource constraint
    X : pd.DataFrame, optional
        A data frame with the alternative-specific variables 
        (e.g., attributes), by default None
    Z : pd.DataFrame, optional
        A data frame with the individual-specific variables, by default None
    """
    # Init function
    def __init__(self,Y: pd.DataFrame,  C: pd.DataFrame, B: float, X: pd.DataFrame = None, Z: pd.DataFrame = None):
        
        # Array of choices
        self.Y = Y.to_numpy().astype(bool)
        
        # Get scalars N and J
        self.N = self.Y.shape[0]
        self.J = self.Y.shape[1]

        # Define array or budget
        self.B = B

        # Define arrays of costs and totalcosts
        self.C = C.to_numpy()
        self.Totalcosts = (self.C * self.Y).sum(axis=1)

        # Define arrays of cases
        self.Case1 = (self.Totalcosts < self.B).astype(bool)
        self.Case2 = ~self.Case1

        # Define variable of remaining resources and log(C)
        self.Remaining = self.B - self.Totalcosts
        self.log_Price = np.log(self.C)

        # Define No. of non-selected alternatives
        self.N_nonchosen = self.J - self.Y.sum(axis=1)

        # Define array for alternative-specific covariates and shape K (if present)
        if X is not None:
            self.K = int(X.shape[1]/self.J)
            self.X = X.to_numpy().reshape((self.N,self.J,self.K))
        else:
            self.K = 0
            self.X = None

        # Define array of individual-specific covariates (if present)
        if Z is not None:
            self.Z = Z.to_numpy()
        else:
            self.Z = None

    # Estimate function
    def estimate(self, startv: np.ndarray, asc: np.ndarray, beta_j: np.ndarray = None, delta_0: float = None, sigma: float = None, alpha_0: float = None, gamma_0: float = None, hess: bool = True, tol: float = 1e-6, diffeps: float = (np.finfo(float).eps)**(1/3), verbose: bool = True):
        """Estimate portfolio KT model

        It starts the optimisation routine of the portfolio KT model. 
        The user can specify the presence of alternative-specific constants 
        (`asc`), separate parameters for the alternative-specific variables 
        (`beta_j`), the presence of a parameter that captures the marginal 
        utility of non-spent resources (`delta_0`), the scale (`sigma`), 
        the satiation (`alpha_0`) and translation (`delta_0`) parameters.

        Parameters
        ----------
        startv : np.ndarray
            Starting values for the maximum-likelihood estimation routine.
        asc : np.ndarray
            An array of length `n_alternatives`, in which each element can
            be either equal to one if the ASC of the corresponding alternative 
            is estimated, and zero otherwise.
        beta_j : np.ndarray, optional
            An array of dimension `n_alternatives*n_attributes`, in which each 
            element can be either equal to one if the corresponding 
            alternative-specific parameter is estimated, and zero otherwise. 
            If `beta_j = None` and `X` exists then single attribute-specific 
            parameters (i.e., equal across alternatives) are estimated 
            , by default None
        delta_0 : float, optional
            If `delta_0` is a float, then the parameter is fixed to the value 
            of `delta_0`, by default None
        sigma : float, optional
            If `sigma` is a float, then the parameter is fixed to the value 
            of `sigma`, otherwise is estimated as `exp(sigma)`, by default None
        alpha_0 : float, optional
            If `alpha_0` is a float, then the parameter is fixed to the value 
            of `alpha_0`, otherwise is estimated as `1/(1+exp(-alpha_0))`, 
            by default None
        gamma_0 : float, optional
            If `gamma_0` is a float, then the parameter is fixed to the value 
            of `gamma_0`, otherwise is estimated as `exp(gamma_0)`, by default None
        hess : bool, optional
            Whether the finite-difference hessian is estimated at the end of the 
            estimation routine, by default True
        tol : float, optional
            Tolerance of the gradient in the estimation routine, by default 1e-6
        diffeps : float, optionsl
            Step size of the finite-difference methods (i.e., gradient and Hessian), 
            by detault `np.sqrt(np.finfo(float).eps)`
        verbose : bool, optional
            Whether the estimation routine returns information at each iteration. 
            See the documentation of `scipy.optimize.minimize` with method 
            `l-bfgs-b` for more information, by default True

        Returns
        -------
        ll : float
            Log-likelihood function at the optimum
        coef : numpy.ndarray
            Estimated parameters at the optimum
        se : numpy.ndarray
            Standard errors of `coef`. If `hess = False` and `method` is 
            not 'bfgsmin' then `se = 0.`, else if method is 'bfgsmin', 
            it returns the standard errors computed from the Hessian 
            approximation.
        hessian : numpy.ndarray
            Finite-difference Hessian. If `hess = False` and `method` is 
            not 'bfgsmin' then `hessian = 0.`, else if method is 'bfgsmin', 
            it returns the Hessian approximation.
            approximation
        diff_time : float
            Estimation time in seconds.
        """
        # Retrieve parameter specifications and store in object
        self.asc = asc
        self.beta_j = beta_j
        self.delta_0 = delta_0
        self.sigma = sigma
        self.alpha_0 = alpha_0
        self.gamma_0 = gamma_0

        # Set arguments for the estimation routine
        args = (self.N,self.J,self.K,self.Y,self.log_Price,self.Remaining,self.N_nonchosen,self.Case1,self.Case2,self.X,self.Z,self.asc,self.beta_j,self.delta_0,self.sigma,self.alpha_0,self.gamma_0)

        # Minimise the LL function
        time0 = time.time()

        res = _bfgsmin(PortKT._llf,startv,tol=tol,verbose=verbose,difftype='forward',diffeps=diffeps,args=args)
        
        # Get/compute outputs
        ll = res['fun']
        self.coef = res['x'].flatten()

        if verbose:
            print('Computing Hessian')

        if hess:
            hessian = Hessian(PortKT._llf,eps=diffeps)(self.coef,self.N,self.J,self.K,self.Y,self.log_Price,self.Remaining,self.N_nonchosen,self.Case1,self.Case2,self.X,self.Z,self.asc,self.beta_j,self.delta_0,self.sigma,self.alpha_0,self.gamma_0)
            se = np.sqrt(np.diag(np.linalg.inv(hessian))).flatten()
        else:
            hessian = res['hessian']
            se = np.sqrt(np.diag(np.linalg.inv(hessian))).flatten()

        time1 = time.time()
        diff_time = time1-time0

        # Return results
        return ll, self.coef, se, hessian, diff_time

    # Finite-difference Hessian
    def hessian(self, eps: float = (np.finfo(float).eps)**(1/3)):
        hess = Hessian(PortKT._llf,eps=eps)(self.coef,self.N,self.J,self.K,self.Y,self.log_Price,self.Remaining,self.N_nonchosen,self.Case1,self.Case2,self.X,self.Z,self.asc,self.beta_j,self.delta_0,self.sigma,self.alpha_0,self.gamma_0)
        return hess

    def optimal_portfolio(self):
        raise TypeError("Optimal portfolio is not implemented yet")

    # Log-likelihood function
    @staticmethod
    def _llf(pars,N,J,K,Y,log_Price,Remaining,N_nonchosen,Case1,Case2,X,Z,asc,beta_j,delta_0,sigma,alpha_0,gamma_0):
        
        # Separate parameters of pars
        par_count = 0

        # Alternative-specific constants
        delta_j = np.zeros(J)
        for j in range(J):
            if asc[j] == 1:
                delta_j[j] = pars[par_count]
                par_count += 1

        # Attribute-specific parameters
        if X is not None:
            if beta_j is not None:
                beta = np.zeros(beta_j.shape)
                for j in range(J):
                    for k in range(K):
                        if beta_j[j,k] == 1:
                            beta[j,k] = pars[par_count]
                            par_count += 1
                Xb = np.sum(X * beta,axis=2)
            else:
                beta = pars[par_count:(K+par_count)]                
                Xb = X @ beta
                par_count += K
        else:
            beta= 0.
            Xb = 0.

        # Individual-specific parameters
        if Z is not None:
            theta = np.vstack([np.zeros(Z.shape[1]), pars[par_count:].reshape(((J-1),Z.shape[1]))])
            Zt = Z @ theta.T
        else:
            theta = 0.
            Zt = 0.

        # Cost parameter
        if delta_0 is None:
            delta_0 = pars[par_count]
            par_count += 1

        # Scale parameter
        if sigma is None:
            sigma = np.exp(pars[par_count])
            par_count += 1

        # Satiation parameter
        if alpha_0 is None:
            alpha_0 = 1/(1+np.exp(-pars[par_count]))
            par_count += 1

        # Satiation parameter
        if gamma_0 is None:
            gamma_0 = np.exp(pars[par_count])
            par_count += 1

        # Initialise log-likelihood
        ll_n = np.zeros(N)

        # Calculate price-normalized marginal utilities
        V0 = delta_0 + (alpha_0-1)*np.log((Remaining/gamma_0)+1)
        Vd = delta_j + Xb + Zt - log_Price

        # Compute log-likelihood of case 1
        if np.any(Case1):
            Wnk0 = np.exp(-((Vd[Case1,:]-V0[Case1,np.newaxis])/sigma))

            sumW0k = np.sum(Wnk0*Y[Case1,:],axis=1)

            elemS = np.sum(1-Y[Case1,:],axis=1)
            cases = np.unique(elemS)

            NoChoice_logical_Case1 = ~Y[Case1,:]

            for j in range(len(cases)):

                if cases[j] == 0:
                    elemS0=(elemS==0)
                    Case10 = (Case1*(N_nonchosen==0))

                    ll_n[Case10] = -np.log((1+sumW0k[elemS0]))

                else:

                    elemSj = (elemS==cases[j])
                    Case1j = elemSj

                    Case1j_long = Case1 * (N_nonchosen==cases[j])

                    NoChoice_logical_1j = NoChoice_logical_Case1[Case1j,:]
                    Wnk0_1j = Wnk0[Case1j,:]

                    Wnk0_1j_select = Wnk0_1j[NoChoice_logical_1j]
                    Wnk0_1j_select.shape = (np.sum(Case1j),cases[j])

                    setS = fullfact(np.repeat(2,cases[j]))
                    elem_setS = np.sum(setS,axis=1)

                    setS_Wnk0 = setS @ Wnk0_1j_select.T

                    term1 = (-1)**elem_setS
                    term2 = (1 + (sumW0k[elemSj] + setS_Wnk0)).T**-1

                    ll_n[Case1j_long] = np.log(np.sum(term1*term2,axis=1))

        # Case 2
        if np.any(Case2):
            LS_select=(Vd[Case2,]*(Y[Case2,]))/sigma
            LS_select=sigma*np.log(np.sum(np.exp(-LS_select),axis=1)-np.sum(1-Y[Case2,],axis=1))

            W0j = np.exp(-((Vd[Case2,:] + LS_select[:,np.newaxis])/sigma))
            W0LS = np.exp(-((V0[Case2]+LS_select)/sigma))

            elemS = np.sum(1-Y[Case2,:],axis=1) + 1
            cases = np.unique(elemS)

            NoChoice_logical_Case2 = ~Y[Case2,:]

            for j in range(len(cases)):

                Case2j = (elemS==cases[j])
                Case2j_long = Case2 * (N_nonchosen==(cases[j]-1))
                NoChoice_logical_2j = NoChoice_logical_Case2[Case2j,:]

                NoChoice_logical_all_2j = np.c_[NoChoice_logical_2j,np.ones(sum(Case2j))].astype(bool)

                W0j_2j = W0j[Case2j,:]
                W0LS_2j = W0LS[Case2j]
                Wall_2j = np.c_[W0j_2j,W0LS_2j]

                W0j_2j_select = Wall_2j[NoChoice_logical_all_2j]
                W0j_2j_select.shape = (np.sum(Case2j),cases[j])

                setS = fullfact(np.repeat(2,cases[j]))
                elem_setS = np.sum(setS,axis=1)

                setS_W0j = setS @ W0j_2j_select.T

                term1 = (-1)**elem_setS
                term2 = (1 + setS_W0j.T)**-1

                ll_n[Case2j_long] = np.log(np.sum(term1*term2,axis=1))

        # Return ll
        return -sum(ll_n)

# Utility functions method
def _utility(pars,J,K,M,Y,C,B_min,B_max,X,Z,combinations,interactions,Totalcosts,Feasible,asc,common_asc,delta_0,beta_j,return_chosen=True):

            # Separate parameters of pars
            par_count = 0

            # Alternative-specific constants
            delta_j = np.zeros(J)
            for j in range(J):
                if asc[j] == 1:
                    delta_j[j] = pars[par_count]
                    par_count += 1

            # Common ASCs
            if common_asc is not None:
                for i in common_asc:
                    delta_j[i] = pars[par_count]
                    par_count +=1

            # Alternative-interaction parameters
            if interactions is not None:
                delta_ij = pars[par_count:(len(interactions)+par_count)]
                par_count += len(interactions)

            # Attribute-specific parameters
            if X is not None:
                if beta_j is not None:
                    beta = np.zeros(beta_j.shape)
                    for j in range(J):
                        for k in range(K):
                            if beta_j[j,k] == 1:
                                beta[j,k] = pars[par_count]
                                par_count += 1
                    Xb = np.sum(X * beta,axis=2)
                else:
                    beta = pars[par_count:(K+par_count)]                
                    Xb = X @ beta
                    par_count += K
            else:
                Xb = 0.

            # Individual-specific parameters
            if Z is not None:
                theta = pars[par_count:(par_count+J*M)].reshape((J,M))
                Zt = Z @ theta.T
            else:
                Zt = 0.

            # Cost parameter
            if delta_0 is None:
                delta_0 = pars[par_count]
                par_count += 1

            # Construct individual utility functions
            Vj = delta_j + Xb + Zt

            # If dimension of Vp is 1, then project along 
            if Vj.ndim == 1:
                Vj = np.tile(Vj,(Feasible.shape[0],1))

            # Construct utility functions of the portfolios
            Vp = Vj @ combinations.T

            if interactions is not None:
                for s in range(len(interactions)):
                    syn = ' & '.join(['(combinations[:,' + str(ss) + ']==1)' for ss in interactions[s]])
                    Vp = Vp + eval(syn)*delta_ij[s]

            if return_chosen:
                Vp_chosen = np.sum(Vj*Y,axis=1)

                if interactions is not None:
                    for s in range(len(interactions)):
                        syn = ' & '.join(['(Y[:,' + str(ss) + ']==1)' for ss in interactions[s]])
                        Vp_chosen = Vp_chosen + eval(syn)*delta_ij[s]

            # if B_max is not None:
            #     Vp += delta_0*(B_max-Totalcosts.T).T
            #     Vp[~Feasible] = -np.inf
            #     if return_chosen:
            #         Vp_chosen += delta_0*(B-np.sum(C*Y,axis=1))
            # else:
                # Vp -= delta_0*Totalcosts
                # if return_chosen:
                #     Vp_chosen -= delta_0*np.sum(C*Y,axis=1)

            Vp += delta_0*Totalcosts
            Vp[~Feasible] = -np.inf

            if return_chosen:
                Vp_chosen += delta_0*np.sum(C*Y,axis=1)

            # Return utility functions
            if return_chosen:
                return Vp, Vp_chosen
            else:
                return Vp