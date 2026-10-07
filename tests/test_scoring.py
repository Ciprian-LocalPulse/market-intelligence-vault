import sys
import unittest
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from common import (DEFAULT_ROOT,load_data,weighted,number,opportunity_score,opportunity_category,
                    confidence_band,evidence_score,freshness,risk_class)
from calculate_scores import calculate

class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load_data(DEFAULT_ROOT)
        cls.scored=calculate(DEFAULT_ROOT,date(2026,10,6),cls.data)

    def test_weighted_endpoints_and_inverse(self):
        model=self.data['09_scores/opportunity_scoring_model.csv']
        best={r['factor']:'0' if r['direction']=='inverse' else '5' for r in model}
        worst={r['factor']:'5' if r['direction']=='inverse' else '0' for r in model}
        self.assertAlmostEqual(weighted(best,model),100)
        self.assertAlmostEqual(weighted(worst,model),0)

    def test_opportunity_formula(self):
        self.assertAlmostEqual(opportunity_score(72*100/95,59),52.4842105263)
        self.assertEqual(opportunity_category(52.4842105263),'WATCH')
        self.assertEqual(opportunity_score(100,0),25)
        self.assertEqual(opportunity_score(100,100),100)

    def test_thresholds(self):
        for score,label in [(85,'PRIORITIZE'),(84.999,'VALIDATE'),(70,'VALIDATE'),(69.999,'EXPLORE'),(55,'EXPLORE'),(40,'WATCH'),(39.999,'DEPRIORITIZE')]:
            self.assertEqual(opportunity_category(score),label)
        for score,label in [(90,'Very High'),(75,'High'),(60,'Moderate'),(40,'Low'),(39.999,'Very Low')]:
            self.assertEqual(confidence_band(score),label)

    def test_invalid_input(self):
        for v in ['',None,'NaN','inf',-1,101,True]:
            with self.subTest(v=v),self.assertRaises(ValueError): number(v)

    def test_freshness_boundaries_unknown_future(self):
        cfg={'default':{'current_days':30,'recent_days':90,'aging_days':180}}
        for pub,expected in [('2026-09-06','Current'),('2026-09-05','Recent'),('2026-07-08','Recent'),('2026-07-07','Aging'),('2026-04-09','Aging'),('2026-04-08','Stale'),('','Unknown')]:
            self.assertEqual(freshness(pub,'unknown',cfg,date(2026,10,6))[0],expected)
        with self.assertRaises(ValueError): freshness('2026-10-07','market',cfg,date(2026,10,6))

    def test_evidence_grades_and_caps(self):
        model=self.data['09_scores/confidence_model.csv']
        row={r['factor']:r['input_max'] for r in model}
        row.update(verification_status='verified',direct_or_indirect='direct',freshness_status='Current',contradiction_flag='false')
        self.assertEqual(evidence_score(row,model),(100,'A'))
        for status,score,grade in [('unsupported',0,'G'),('speculation',19,'F'),('unverified',39,'E')]:
            self.assertEqual(evidence_score({**row,'verification_status':status},model),(score,grade))
        self.assertEqual(evidence_score({**row,'direct_or_indirect':'indirect'},model),(74,'C'))
        self.assertEqual(evidence_score({**row,'freshness_status':'Stale'},model),(39,'D'))
        self.assertEqual(evidence_score({**row,'freshness_status':'Unknown'},model),(59,'D'))

    def test_risk_formula_and_catastrophic_override(self):
        row=self.scored['06_risks/risk_register.csv'][0]
        self.assertEqual(float(row['risk_score']),75)
        self.assertEqual(row['classification'],'High')
        self.assertEqual([float(r['risk_score']) for r in self.scored['06_risks/risk_register.csv']],[75,66,72])
        self.assertEqual(risk_class(40,{**row,'impact':'5','likelihood':'3'}),'Critical')
        self.assertEqual(risk_class(1,{**row,'override':'true'}),'Critical')

    def test_all_scores_in_range(self):
        for path,rows in self.scored.items():
            for row in rows:
                for field,value in row.items():
                    if field.endswith('_score') and value:
                        self.assertGreaterEqual(float(value),0)
                        self.assertLessEqual(float(value),100)

    def test_conflict_and_independence(self):
        evidence={r['evidence_id']:r for r in self.scored['08_evidence/evidence_register.csv']}
        claims={r['claim_id']:r for r in self.scored['08_evidence/claims_register.csv']}
        self.assertEqual(float(evidence['EV-001']['corroboration_score']),0)
        self.assertEqual(float(evidence['EV-001']['confidence_score']),75)
        self.assertEqual(float(claims['CLM-001']['confidence_score']),59)

    def test_recomputation_idempotent(self):
        self.assertEqual(self.scored,calculate(DEFAULT_ROOT,date(2026,10,6),self.scored))

    def test_other_model_worked_values(self):
        self.assertEqual(float(self.scored['02_market/market_assessment.csv'][0]['market_attractiveness_score']),53.2)
        self.assertEqual([float(r['competitor_pressure_score']) for r in self.scored['03_competitors/competitor_database.csv']],[66,60.8,55.6])
        self.assertEqual(float(self.scored['05_opportunities/gap_register.csv'][0]['gap_score']),68.85)
        self.assertEqual([float(r['opportunity_score']) for r in self.scored['05_opportunities/opportunity_database.csv']],[52.48,47.4,33.53])
        self.assertEqual(float(self.scored['07_strategy/recommendations.csv'][0]['confidence_score']),59)

    def test_missing_factor_rejected(self):
        model=self.data['09_scores/opportunity_scoring_model.csv']
        row={r['factor']:'3' for r in model}; row['market_demand']=''
        with self.assertRaises(ValueError): weighted(row,model)

if __name__=='__main__': unittest.main()
