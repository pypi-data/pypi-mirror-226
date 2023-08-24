import sys
import os
sys.path.append(os.getcwd())
import unittest
from cleaning_functions import *
from searchdatamodels import EducationExperience, WorkExperience

class CleaningTest(unittest.TestCase):
    def test_summary_name_token_replacement(self):
        education_list=[EducationExperience(Degree="phd", Institution="university of toronto")]
        work_list=[WorkExperience(Institution="self-employed", Specialization="mercenary")]
        cand=Candidate(Name="wade wilson", EducationExperienceList=education_list, WorkExperienceList=work_list)
        self.assertNotEqual(0, cand.Summary.Text.count(NAME_TOKEN))
        self.assertEqual(0, cand.Summary.Text.count(cand.Name))
        cand=summary_name_token_replacement(cand=cand)
        self.assertEqual(0, cand.ExternalSummaryStr.count(NAME_TOKEN))
        self.assertNotEqual(0, cand.ExternalSummaryStr.count(cand.Name))

    def test_summary_name_token_replacement_candidate_list(self):
        education_list=[EducationExperience(Degree="phd", Institution="university of toronto")]
        work_list=[WorkExperience(Institution="self-employed", Specialization="mercenary")]
        candidate_list=[Candidate(Name="wade wilson", EducationExperienceList=education_list, WorkExperienceList=work_list) for _ in range(3)]
        candidate_list=summary_name_token_replacement_candidate_list(candidate_list)
        for cand in candidate_list:
            self.assertNotEqual(0, cand.Summary.Text.count(NAME_TOKEN))
            self.assertEqual(0, cand.Summary.Text.count(cand.Name))
            self.assertEqual(0, cand.ExternalSummaryStr.count(NAME_TOKEN))
            self.assertNotEqual(0, cand.ExternalSummaryStr.count(cand.Name))


if __name__=='__main__':
    unittest.main()