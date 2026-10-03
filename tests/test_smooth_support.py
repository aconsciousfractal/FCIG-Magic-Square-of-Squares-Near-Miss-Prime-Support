"""Deliberate corruptions and positive controls. No network or CAS is needed."""
import copy
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checker_under_test', ROOT/'scripts/verify_smooth_support.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class ExactCheckerControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.abc = json.loads((ROOT/'certificates/smooth_support/abc_S19.json').read_text())

    def expect_fail(self, action, prefix):
        with self.assertRaises(v.VerificationError) as context:
            action()
        self.assertTrue(str(context.exception).startswith(prefix), str(context.exception))
        print('EXPECTED REJECTION:', str(context.exception))

    def test_01_complete_certificate_passes(self):
        self.assertEqual(len(v.validate_abc(self.abc, 19)), 3649)

    def test_02_deleted_row_is_not_complete(self):
        self.expect_fail(lambda:v.validate_abc(self.abc[:-1],19),'COUNT:')

    def test_03_duplicate_does_not_fill_a_cardinality_gap(self):
        data = copy.deepcopy(self.abc)
        data[-1] = data[-2]
        self.expect_fail(lambda:v.validate_abc(data,19),'DUPLICATE:')

    def test_04_wrong_addition(self):
        data = copy.deepcopy(self.abc); data[0] = [1,1,3]
        self.expect_fail(lambda:v.validate_abc(data,19),'ADDITION:')

    def test_05_common_factor_not_primitive(self):
        data = copy.deepcopy(self.abc); data[0] = [2,2,4]
        self.expect_fail(lambda:v.validate_abc(data,19),'PRIMITIVITY:')

    def test_06_prime_23_not_allowed(self):
        data = copy.deepcopy(self.abc); data[0] = [1,22,23]
        self.expect_fail(lambda:v.validate_abc(data,19),'SUPPORT:')

    def test_07_zero_cannot_enter_a_unit_equation(self):
        data = copy.deepcopy(self.abc); data[0] = [0,1,1]
        self.expect_fail(lambda:v.validate_abc(data,19),'DOMAIN:')

    def test_08_bool_is_not_an_integer_certificate(self):
        data = copy.deepcopy(self.abc); data[0] = [True,1,2]
        self.expect_fail(lambda:v.validate_abc(data,19),'DOMAIN:')

    def test_09_short_finite_list_cannot_be_promoted(self):
        self.expect_fail(lambda:v.validate_abc([[1,1,2]],19),'COUNT:')

    def test_10_undeclared_import_is_blocked(self):
        self.expect_fail(lambda:v.validate_abc(self.abc,23),'IMPORT:')

    def test_11_midpoint_detector_positive_control(self):
        count,hits = v.midpoint_hits([Q(1),Q(2),Q(3)])
        self.assertEqual((count,hits),(3,[[Q(1),Q(2),Q(3)]]))

    def test_12_midpoint_detector_negative_control(self):
        self.assertEqual(v.midpoint_hits([Q(1),Q(2),Q(4)]),(3,[]))

    def test_13_duplicate_centres_rejected(self):
        self.expect_fail(lambda:v.midpoint_hits([Q(1),Q(1),Q(2)]),'CENTRES:')

    def test_14_irrational_square_root_rejected(self):
        self.expect_fail(lambda:v.rational_square_root(Q(2)),'ROOT:')

    def test_15_degenerate_array_not_9_7(self):
        self.expect_fail(lambda:v.line_data((1,)*9),'LINES:')

    def test_16_produced_triangle_atlas_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)/'certificates'; shutil.copytree(ROOT/'certificates/smooth_support',work)
            path = work/'triangles_S7.json'; data=json.loads(path.read_text());data.pop()
            path.write_text(json.dumps(data))
            self.expect_fail(lambda:v.run(work),'TRIANGLE_ATLAS_MISMATCH:')

    def test_17_produced_array_atlas_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)/'certificates';shutil.copytree(ROOT/'certificates/smooth_support',work)
            path=work/'atlas_9_7_S7.json';data=json.loads(path.read_text());data[0]['d']+=1
            path.write_text(json.dumps(data))
            self.expect_fail(lambda:v.run(work),'ARRAY_ATLAS_MISMATCH:')

    def test_18_full_independent_reconstruction(self):
        result=v.run(ROOT/'certificates/smooth_support')
        self.assertEqual(result,json.loads((ROOT/'certificates/smooth_support/expected_verification.json').read_text()))

    def test_19_integer_float_and_boolean_certificates_differ(self):
        self.assertFalse(v.exact_json_equal({'d': 1}, {'d': 1.0}))
        self.assertFalse(v.exact_json_equal({'d': 1}, {'d': True}))

    def test_20_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'duplicate.json'; path.write_text('{"d": 2, "d": 1}')
            self.expect_fail(lambda:v.read_json(path),'JSON:')

    def test_21_float_triangle_atlas_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)/'certificates';shutil.copytree(ROOT/'certificates/smooth_support',work)
            path=work/'triangles_S7.json';data=json.loads(path.read_text());data[0]['m']=float(data[0]['m'])
            path.write_text(json.dumps(data))
            self.expect_fail(lambda:v.run(work),'TRIANGLE_ATLAS_MISMATCH:')

    def test_22_aebi_squareclass_consequence_and_sharpness(self):
        # Completeness of these seven primitive triangles is imported from Aebi.
        # This check validates only the exact arithmetic used in the consequence.
        cores=((3,4,5),(5,12,13),(8,15,17),(9,40,41),(7,24,25),(16,63,65),(17,144,145))
        areas=[]; kernels=[]
        for a,b,c in cores:
            self.assertEqual(a*a+b*b,c*c)
            self.assertEqual(v.gcd(a,b),1)
            area=a*b//2; areas.append(area)
            vals,rest=v.factor_over(area,v.PRIMES)
            self.assertEqual(rest,1)
            kernel=1
            for p,e in zip(v.PRIMES,vals): kernel*=p**(e%2)
            kernels.append(kernel)
            self.assertEqual(c*c-(a-b)**2,4*area)
            self.assertEqual((a+b)**2-c*c,4*area)
        self.assertEqual(areas,[6,30,60,180,84,504,1224])
        self.assertEqual(kernels,[6,30,15,5,21,14,34])
        self.assertEqual(len(set(kernels)),7)
        for r,s,t in ((1,29,41),(23,37,47)):
            self.assertEqual((s*s-r*r,t*t-s*s),(840,840))

if __name__=='__main__':unittest.main(verbosity=2)
