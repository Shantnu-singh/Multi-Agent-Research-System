import ast

# Example response string
response = '''python
{
  "webpages": ["https://www.irena.org/", "https://www.seia.org/", "https://www.iea.org/"],
  "youtube": "https://www.youtube.com/results?search_query=latest+trends+in+renewable+energy"
}
'''

# Convert the string to a Python dictionary
# data = ast.literal_eval(response.strip())  # .strip() removes any leading/trailing whitespace

# print()
# print(type(data))  # Output: <class 'dict'>
print(response.strip("{"))