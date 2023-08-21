# odysseus_ai

system_message = "You are a helpful assistant that translates English to French."
model = 'gpt-3.5'
init(project_name='test',prompt=system_message, model=model)
log(project_name='test',input_llm='Hello world', output_llm='hey')



 python setup.py sdist bdist_wheel

 twine upload dist/*

 rm -rf dist/*