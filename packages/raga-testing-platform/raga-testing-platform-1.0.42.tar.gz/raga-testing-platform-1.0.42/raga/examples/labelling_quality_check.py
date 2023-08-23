from raga import *

test_session = TestSession(project_name="testingProject",
                           run_name="labelling-run-18-aug-v8")

rules = LQRules()
rules.add(metric="loss", label=["All"], metric_threshold=0.005)


edge_case_detection = labelling_quality_test(test_session=test_session,
                                            dataset_name = "labelling-dataset-18-aug-v1",
                                            test_name = "Test",
                                            type = "labelling_consistency",
                                            rules = rules)
test_session.add(edge_case_detection)

test_session.run()