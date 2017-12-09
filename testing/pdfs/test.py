from django.template.loader import render_to_string

from weasyprint import HTML

from tempfile import NamedTemporaryFile

from .file_handlers import FileHandler


def get_temp_file(data):
	tf = NamedTemporaryFile(mode = "w",suffix = ".svg")
	tf.write(data)
	tf.seek(0)
	return tf

def generate_file():
	tpl = "diet.html"

	svg_tpl = "dial.svg"

	file_tpl = "file://%s"

	protein = render_to_string(svg_tpl,{
		"percentage" : 500
	})
	carbs = render_to_string(svg_tpl,{
		"percentage" : 500
	})
	fat = render_to_string(svg_tpl,{
		"percentage" : 500
	})

	carbs_file = get_temp_file(carbs)
	protein_file = get_temp_file(protein)
	fat_file = get_temp_file(fat)

	pdf = render_to_string(tpl , {
		"protein" : file_tpl%protein_file.name,
		"fat" : file_tpl%fat_file.name,
		"carbs" : file_tpl%carbs_file.name,
	})


	pdf = HTML(string = pdf).write_pdf()

	file = FileHandler.save(
		pdf,
		extension = "pdf"
	)
