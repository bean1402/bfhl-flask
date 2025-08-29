from flask import Flask, request, jsonify
import os

app = Flask(__name__)

FULL_NAME = os.getenv("FULL_NAME", "john_doe")        
DATE_OF_BIRTH = os.getenv("DOB_DDMMYYYY", "17091999")
EMAIL_ADDRESS = os.getenv("EMAIL", "john@xyz.com")
STUDENT_ROLL = os.getenv("ROLL_NUMBER", "ABCD123")

def check_integer_format(value):
   if isinstance(value, int):
       return True
   if isinstance(value, str):
       cleaned_value = value.strip()
       if cleaned_value.startswith(('+', '-')):
           return cleaned_value[1:].isdigit()
       return cleaned_value.isdigit()
   return False

def check_alphabetic_only(value):
   return isinstance(value, str) and len(value) > 0 and value.isalpha()

@app.post("/bfhl")
def process_bfhl_request():
   try:
       request_data = request.get_json(force=True, silent=False)
   except Exception:
       return jsonify({"is_success": False, "error": "Invalid JSON format"}), 400

   if not isinstance(request_data, dict) or "data" not in request_data:
       return jsonify({"is_success": False, "error": "Missing required 'data' field"}), 400

   input_data = request_data["data"]
   if not isinstance(input_data, list):
       return jsonify({"is_success": False, "error": "'data' field must be an array"}), 400

   even_number_list = []
   odd_number_list = []
   total_sum = 0
   alphabet_list = []
   special_char_list = []
   letter_collection = []

   for element in input_data:
       if check_integer_format(element):
           numeric_value = int(element)
           total_sum += numeric_value
           (even_number_list if numeric_value % 2 == 0 else odd_number_list).append(str(numeric_value))
       elif check_alphabetic_only(element):
           alphabet_list.append(element.upper())
           letter_collection.extend(list(element))
       elif isinstance(element, str) and len(element) > 0 and all(not char.isalnum() for char in element):
           special_char_list.append(element)
       else:
           special_char_list.append(str(element))

   reversed_letters = list(reversed(letter_collection))
   alternating_case = []
   for index, character in enumerate(reversed_letters):
       alternating_case.append(character.upper() if index % 2 == 0 else character.lower())
   concatenated_result = "".join(alternating_case)

   api_response = {
       "is_success": True,
       "user_id": f"{FULL_NAME.lower()}_{DATE_OF_BIRTH}",
       "email": EMAIL_ADDRESS,
       "roll_number": STUDENT_ROLL,
       "odd_numbers": odd_number_list,
       "even_numbers": even_number_list,
       "alphabets": alphabet_list,
       "special_characters": special_char_list,
       "sum": str(total_sum),
       "concat_string": concatenated_result,
   }
   return jsonify(api_response), 200

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)