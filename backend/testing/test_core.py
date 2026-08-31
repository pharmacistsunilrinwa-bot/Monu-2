import unittest
from backend.services.monitoring_services import HealthMonitorService

class TestCoreComponents(unittest.TestCase):
    def test_health_monitor(self):
        monitor = HealthMonitorService()
        health = monitor.get_health()
        self.assertEqual(health["status"], "OPERATIONAL")

if __name__ == '__main__':
    unittest.main()
