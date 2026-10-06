"""Ensure assembly checks reject meaningful broken configurations in session layers."""
import unittest
from pxr import Usd, UsdPhysics
from station_checks import ROOT, PEDESTAL, check_station


class AssemblyRegressions(unittest.TestCase):
    def setUp(self):
        self.stage = Usd.Stage.Open(str(ROOT / "components/robot_station/robot_station.usd"))
        self.stage.SetEditTarget(self.stage.GetSessionLayer())
        self.root = self.stage.GetPrimAtPath("/RobotStation")

    def test_missing_mapping(self):
        rel = self.root.GetRelationship("isaac:physics:robotJoints")
        targets = rel.GetTargets()
        targets[-1] = "/RobotStation/MissingJoint"
        rel.SetTargets(targets)
        with self.assertRaisesRegex(AssertionError, "Missing mapping"):
            check_station(self.stage, "/RobotStation")

    def test_dynamic_pedestal(self):
        UsdPhysics.RigidBodyAPI.Apply(self.stage.GetPrimAtPath("/RobotStation" + PEDESTAL))
        with self.assertRaisesRegex(AssertionError, "Dynamic pedestal"):
            check_station(self.stage, "/RobotStation")

    def test_mount_misalignment(self):
        self.stage.GetPrimAtPath("/RobotStation/ToolMountJoint").GetAttribute("physics:localPos0").Set((1, 0, 0))
        with self.assertRaisesRegex(AssertionError, "Tool mount frames differ"):
            check_station(self.stage, "/RobotStation")

    def test_unlabelled_placeholder(self):
        self.root.GetVariantSet("EndEffector").SetVariantSelection("Vacuum_Gripper")
        self.root.GetAttribute("workcell:toolStatus").Set("implemented")
        with self.assertRaisesRegex(AssertionError, "Unlabelled vacuum"):
            check_station(self.stage, "/RobotStation")


if __name__ == "__main__":
    unittest.main()
