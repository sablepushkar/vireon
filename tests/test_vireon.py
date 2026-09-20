from __future__ import annotations
import unittest
from datetime import datetime, timedelta, timezone
from vireon.ai_guard import ModelSpec, assess_model
from vireon.core.models import EventType, PharmaEvent
from vireon.core.validation import EventValidationError, validate_event
from vireon.digital_measures import validate_digital_measure
from vireon.evidence_graph import EvidenceGraph
from vireon.lifecycle import LifecycleStage, simulate_lifecycle
from vireon.signal_engine import detect_signals
from vireon.trial_integrity import TrialEvent, assess_site

class VireonTests(unittest.TestCase):
    def _event(self, values=None):
        return PharmaEvent("E-001","P-001","S-01",EventType.LAB_RESULT,datetime.now(timezone.utc)-timedelta(minutes=1),values or {"biomarker_x":135.0},"test")
    def test_future_timestamp_is_rejected(self):
        e=self._event(); e=PharmaEvent(e.event_id,e.patient_id,e.site_id,e.event_type,datetime.now(timezone.utc)+timedelta(minutes=5),e.values,e.source)
        with self.assertRaises(EventValidationError): validate_event(e)
    def test_signal_version_and_graph(self):
        e=self._event(); signal=detect_signals([e])[0]; self.assertEqual(signal.detector_version,"threshold-rules/0.2")
        graph=EvidenceGraph(); graph.add_event(e); graph.add_signal(signal); self.assertEqual(len(graph.nodes),2)
    def test_ai_guard_flags_shift(self):
        r=assess_model(ModelSpec("demo","1","research","medium","validated"),[100,100,100],[130,130,130]); self.assertIn("distribution_mean_shift",r.risk_flags)
    def test_digital_measure_flags_missingness(self):
        self.assertIn("high_missingness",validate_digital_measure("m",[1.0,None,None,2.0]).flags)
    def test_trial_integrity_flags_deviation(self):
        now=datetime.now(timezone.utc); r=assess_site("S-01",[TrialEvent("1","S-01",now,"visit",protocol_deviation=True),TrialEvent("2","S-01",now,"lab")]); self.assertEqual(r.status,"review")
    def test_lifecycle_has_all_stages(self):
        result=simulate_lifecycle("C"); self.assertEqual(len(result),len(LifecycleStage)); self.assertEqual(result[-1].stage,LifecycleStage.POST_MARKET)

if __name__=="__main__": unittest.main()
