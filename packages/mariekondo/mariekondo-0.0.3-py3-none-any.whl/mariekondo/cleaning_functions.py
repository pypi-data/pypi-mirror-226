from searchdatamodels import NAME_TOKEN, Candidate
from typing import List

def summary_name_token_replacement(cand: Candidate) -> Candidate:
    '''The function updates the ExternalSummaryStr to be = the summary string but 
    searchdatamodels.NAME_TOKEN has been replaced with the real name
    
    Parameters
    ----------
    cand : Candidate
    
    Returns
    -------
        the updated candidate object with the external summary string
    
    '''
    real_name=cand.Name
    cand.ExternalSummaryStr=cand.Summary.Text.replace(NAME_TOKEN, real_name)
    return cand

def summary_name_token_replacement_candidate_list(candidate_list: List[Candidate])-> List[Candidate]:
    if len(candidate_list)==0:
        return candidate_list
    return [summary_name_token_replacement(c) for c in candidate_list]