import logging
import os
import sys
from flask import Flask, request, render_template

from gemstack_mlops.pipeline.prediction_pipeline import PredictPipeline, CustomData

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route("/compare", methods=["GET", "POST"])
def compare_diamonds():
    """Compare prices of different diamond configurations"""
    if request.method == "GET":
        return render_template("compare.html")
    else:
        try:
            # Get base diamond data
            base_data = CustomData(
                carat=float(request.form.get("base_carat", 1.0)),
                depth=float(request.form.get("base_depth", 60.0)),
                table=float(request.form.get("base_table", 55.0)),
                x=float(request.form.get("base_x", 6.0)),
                y=float(request.form.get("base_y", 6.0)),
                z=float(request.form.get("base_z", 4.0)),
                cut=request.form.get("base_cut", "Ideal"),
                color=request.form.get("base_color", "G"),
                clarity=request.form.get("base_clarity", "VS1")
            )

            # Get comparison diamond data
            compare_data = CustomData(
                carat=float(request.form.get("compare_carat", 1.5)),
                depth=float(request.form.get("compare_depth", 62.0)),
                table=float(request.form.get("compare_table", 58.0)),
                x=float(request.form.get("compare_x", 7.0)),
                y=float(request.form.get("compare_y", 7.0)),
                z=float(request.form.get("compare_z", 4.0)),
                cut=request.form.get("compare_cut", "Premium"),
                color=request.form.get("compare_color", "D"),
                clarity=request.form.get("compare_clarity", "VVS1")
            )

            predict_pipeline = PredictPipeline()

            base_df = base_data.get_data_as_dataframe()
            compare_df = compare_data.get_data_as_dataframe()

            base_price = predict_pipeline.predict(base_df)[0]
            compare_price = predict_pipeline.predict(compare_df)[0]

            price_diff = compare_price - base_price
            percent_diff = (price_diff / base_price) * 100

            return render_template("compare_result.html",
                                 base_price=round(base_price, 2),
                                 compare_price=round(compare_price, 2),
                                 price_diff=round(price_diff, 2),
                                 percent_diff=round(percent_diff, 1),
                                 base_data=base_data,
                                 compare_data=compare_data)

        except Exception as e:
            logging.error("Error during diamond comparison: %s", e)
            return render_template("compare.html", error="An error occurred during comparison. Please check your input and try again.")

@app.route("/predict", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    else:
        try:
            data = CustomData(
                carat=float(request.form.get("carat")),
                depth=float(request.form.get("depth")),
                table=float(request.form.get("table")),
                x=float(request.form.get("x")),
                y=float(request.form.get("y")),
                z=float(request.form.get("z")),
                cut=request.form.get("cut"),
                color=request.form.get("color"),
                clarity=request.form.get("clarity")
            )
            final_data = data.get_data_as_dataframe()

            predict_pipeline = PredictPipeline()
            pred = predict_pipeline.predict(final_data)

            result = round(pred[0], 2)
            return render_template("result.html", final_result=result)

        except Exception as e:
            logging.error("Error during prediction: %s", e)
            return render_template("form.html", error="An error occurred during prediction. Please check your input and try again.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
