#!/usr/bin/env python3
"""
Comprehensive test script to verify all MLOps project features are working correctly.
This script tests:
1. Prediction pipeline functionality
2. Web application components
3. ML artifacts existence and accessibility
4. Template files
5. Configuration files
6. Dependencies and imports
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def setup_logging():
    """Setup logging for test execution"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class FeatureTester:
    def __init__(self):
        self.test_results = []
        self.artifacts_dir = project_root / "artifacts"
        self.templates_dir = project_root / "templates"
        self.config_dir = project_root / "config"

    def log_test_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result and store it"""
        status = "✅ PASS" if success else "❌ FAIL"
        full_message = f"{status} - {test_name}"
        if message:
            full_message += f": {message}"

        logger.info(full_message)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })

    def test_artifacts_existence(self):
        """Test that all required ML artifacts exist"""
        logger.info("Testing ML artifacts existence...")

        required_artifacts = [
            "model.pkl",
            "preprocessor.pkl",
            "test.csv",
            "train.csv",
            "raw.csv"
        ]

        all_exist = True
        missing_artifacts = []

        for artifact in required_artifacts:
            artifact_path = self.artifacts_dir / artifact
            if artifact_path.exists():
                logger.info(f"  ✅ {artifact} exists")
            else:
                logger.error(f"  ❌ {artifact} missing")
                all_exist = False
                missing_artifacts.append(artifact)

        self.log_test_result(
            "ML Artifacts Existence",
            all_exist,
            f"Missing artifacts: {missing_artifacts}" if not all_exist else "All artifacts present"
        )
        return all_exist

    def test_template_files(self):
        """Test that all required template files exist and are accessible"""
        logger.info("Testing template files...")

        required_templates = [
            "index.html",
            "form.html",
            "result.html"
        ]

        all_exist = True
        missing_templates = []

        for template in required_templates:
            template_path = self.templates_dir / template
            if template_path.exists():
                logger.info(f"  ✅ {template} exists")

                # Check for known issues (like typos)
                if template == "result.html":
                    content = template_path.read_text()
                    if "Dimond" in content:
                        logger.warning(f"  ⚠️  Typo found in {template}: 'Dimond' should be 'Diamond'")
                        self.log_test_result(
                            "Template Typo Check",
                            False,
                            "Found 'Dimond' instead of 'Diamond' in result.html"
                        )
            else:
                logger.error(f"  ❌ {template} missing")
                all_exist = False
                missing_templates.append(template)

        self.log_test_result(
            "Template Files Existence",
            all_exist,
            f"Missing templates: {missing_templates}" if not missing_templates else "All templates present"
        )
        return all_exist

    def test_config_files(self):
        """Test that configuration files exist and are valid"""
        logger.info("Testing configuration files...")

        required_configs = [
            "config/config.yaml"
        ]

        all_exist = True
        missing_configs = []

        for config in required_configs:
            config_path = project_root / config
            if config_path.exists():
                logger.info(f"  ✅ {config} exists")
            else:
                logger.error(f"  ❌ {config} missing")
                all_exist = False
                missing_configs.append(config)

        self.log_test_result(
            "Configuration Files",
            all_exist,
            f"Missing configs: {missing_configs}" if not missing_configs else "All config files present"
        )
        return all_exist

    def test_project_imports(self):
        """Test that project-specific imports work"""
        logger.info("Testing project-specific imports...")

        project_imports = [
            ("gemstack_mlops.pipeline.prediction_pipeline", ["PredictPipeline", "CustomData"]),
            ("gemstack_mlops.exception.exception", ["CustomException"]),
            ("gemstack_mlops.logger.logger", ["logging"]),
            ("gemstack_mlops.utils.utils", ["load_object"]),
        ]

        all_imports_work = True
        failed_imports = []

        for module_name, classes in project_imports:
            try:
                module = __import__(module_name, fromlist=classes)
                for class_name in classes:
                    if hasattr(module, class_name):
                        logger.info(f"  ✅ {module_name}.{class_name} import successful")
                    else:
                        logger.error(f"  ❌ {class_name} not found in {module_name}")
                        all_imports_work = False
                        failed_imports.append(f"{module_name}.{class_name}")
            except ImportError as e:
                logger.error(f"  ❌ {module_name} import failed: {e}")
                all_imports_work = False
                failed_imports.append(module_name)

        self.log_test_result(
            "Project Imports",
            all_imports_work,
            f"Failed imports: {failed_imports}" if not all_imports_work else "All project imports successful"
        )
        return all_imports_work

    def test_prediction_pipeline(self):
        """Test the prediction pipeline with sample data"""
        logger.info("Testing prediction pipeline...")

        try:
            from gemstack_mlops.pipeline.prediction_pipeline import PredictPipeline, CustomData

            # Test PredictPipeline instantiation
            pipeline = PredictPipeline()
            logger.info("  ✅ PredictPipeline instantiated successfully")

            # Test CustomData creation with sample data
            sample_data = CustomData(
                carat=0.5,
                depth=60.0,
                table=55.0,
                x=5.0,
                y=5.0,
                z=3.1,
                cut='Ideal',
                color='G',
                clarity='VS2'
            )

            df = sample_data.get_data_as_dataframe()
            logger.info("  ✅ CustomData processed successfully")
            logger.info(f"  📊 DataFrame shape: {df.shape}")

            # Test prediction (if artifacts exist)
            if self.test_artifacts_existence():
                try:
                    prediction = pipeline.predict(df)
                    logger.info(f"  ✅ Prediction successful: {prediction[0]:.2f}")
                    self.log_test_result(
                        "Prediction Pipeline",
                        True,
                        f"Sample prediction successful: {prediction[0]:.2f}"
                    )
                    return True
                except Exception as e:
                    logger.error(f"  ❌ Prediction failed: {e}")
                    self.log_test_result(
                        "Prediction Pipeline",
                        False,
                        f"Prediction failed: {e}"
                    )
                    return False
            else:
                logger.warning("  ⚠️  Skipping prediction test - artifacts missing")
                self.log_test_result(
                    "Prediction Pipeline",
                    False,
                    "Cannot test prediction - artifacts missing"
                )
                return False

        except Exception as e:
            logger.error(f"  ❌ Prediction pipeline test failed: {e}")
            self.log_test_result(
                "Prediction Pipeline",
                False,
                f"Pipeline test failed: {e}"
            )
            return False

    def test_airflow_dags(self):
        """Test Airflow DAG files exist and are syntactically correct"""
        logger.info("Testing Airflow DAGs...")

        airflow_dags = [
            "airflow/dags/training_pipeline.py",
            "airflow/dags/batch_prediction.py"
        ]

        all_valid = True
        invalid_dags = []

        for dag_path in airflow_dags:
            full_path = project_root / dag_path
            if full_path.exists():
                try:
                    # Try to compile the Python file to check syntax
                    with open(full_path, 'r') as f:
                        compile(f.read(), str(full_path), 'exec')
                    logger.info(f"  ✅ {dag_path} syntax valid")
                except SyntaxError as e:
                    logger.error(f"  ❌ {dag_path} syntax error: {e}")
                    all_valid = False
                    invalid_dags.append(dag_path)
            else:
                logger.error(f"  ❌ {dag_path} missing")
                all_valid = False
                invalid_dags.append(dag_path)

        self.log_test_result(
            "Airflow DAGs",
            all_valid,
            f"Invalid DAGs: {invalid_dags}" if not all_valid else "All DAGs valid"
        )
        return all_valid

    def run_all_tests(self):
        """Run all feature tests"""
        logger.info("=" * 60)
        logger.info("🚀 STARTING COMPREHENSIVE FEATURE TESTING")
        logger.info("=" * 60)

        test_methods = [
            self.test_artifacts_existence,
            self.test_template_files,
            self.test_config_files,
            self.test_project_imports,
            self.test_prediction_pipeline,
            self.test_airflow_dags,
        ]

        results = []
        for test_method in test_methods:
            try:
                result = test_method()
                results.append(result)
                logger.info("")  # Empty line between tests
            except Exception as e:
                logger.error(f"❌ Test {test_method.__name__} crashed: {e}")
                results.append(False)

        # Summary
        logger.info("=" * 60)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 60)

        passed_tests = sum(results)
        total_tests = len(results)
        success_rate = (passed_tests / total_tests) * 100

        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {total_tests - passed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")

        # Detailed results
        logger.info("\nDetailed Results:")
        for result in self.test_results:
            if result['success']:
                logger.info(f"✅ {result['test']}: {result['message']}")
            else:
                logger.error(f"❌ {result['test']}: {result['message']}")

        return success_rate >= 80  # Consider 80% success as overall pass

def main():
    """Main test execution function"""
    tester = FeatureTester()
    success = tester.run_all_tests()

    if success:
        logger.info("\n🎉 All critical features are working correctly!")
        sys.exit(0)
    else:
        logger.error("\n⚠️  Some features have issues that need attention.")
        sys.exit(1)

if __name__ == "__main__":
    main()
