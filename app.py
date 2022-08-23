import joblib as joblib
from flask import Flask, render_template, request, jsonify

from ease import util_functions
from ease.grade import grade
import json

app = Flask(__name__)

totalScoreModel = joblib.load('model_for_chongjum.pkl')
dockhaeModel = joblib.load('model_for_dockhae.pkl')
nonliModel = joblib.load('model_for_nonli.pkl')
pyohyunModel = joblib.load('model_for_pyohyun.pkl')

@app.route('/')
def hello():
	return render_template('main.html')

@app.route("/submit", methods=['POST'])
def submit():
	if (request.method == 'POST'):
		value = request.form.get('essayContent')
		cleanedText = util_functions.sub_chars(value)

		totalScore = grade(totalScoreModel, cleanedText)
		dockhaeScore = grade(dockhaeModel, cleanedText)
		nonliScore = grade(nonliModel, cleanedText)
		pyohyunScore = grade(pyohyunModel, cleanedText)
		scores = {
			"message": "Success",
			"response": {
				"totalScore": totalScore["score"],
				"logicScore": nonliScore["score"],
				"expressionScore": pyohyunScore["score"],
				"vocabularyScore": dockhaeScore["score"],
			}
		}
		#scores = jsonify(scores)
		return render_template("gradeSheet.html", scores=scores)
	#return jsonify()
	# if (request.method == 'POST'):
	# 	value = request.form["essayContent"]
	# 	value = json.loads(value.decode('utf-8'))
	# 	#model = joblib.load('model.pkl')
	# 	value = util_functions.sub_chars(value["essayContent"])
	# 	#score = grade(model, value)
	# 	print(value)
	# 	result = {
	# 		"message": "Success",
	# 		"response": {
	# 			"totalScore": 3,
	# 			"logicScore": 3,
	# 			"expressionScore": 3,
	# 			"vocabularyScore": 3,
	# 		}
	# 	}
	# 	return jsonify(result)





if __name__ == '__main__':
    app.run()
