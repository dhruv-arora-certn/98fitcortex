import subprocess , sys
import click , sqlalchemy

def update_table(table , url):
	click.secho("Fixing Data " ,  fg = "red")
	engine = sqlalchemy.create_engine(url)
	with engine.connect() as con:
		con.execute("alter table %s alter column calarie type float using cast(calarie as float)"%table)	
		con.execute("alter table %s alter column weight type float using cast(weight as float)"%table)	
		con.execute("alter table %s alter column quantity type integer using cast(quantity as integer)"%table)	
		con.execute("alter table %s alter column protein type float using cast(protein as float)"%table)	
		con.execute("alter table %s alter column fat type float using cast(fat as float)"%table)	
		con.execute("alter table %s alter column carbohydrates type float using cast(carbohydrates as float)"%table)	
		con.execute("alter table %s alter column nuts type integer using cast(nuts as integer)"%table)
		con.execute("alter table %s alter column for_loss type integer using cast(for_loss as integer)"%table)	
		con.execute("alter table %s alter column pulses type integer using cast(pulses as integer)"%table)	
		con.execute("alter table %s alter column pulses type integer using cast(pulses as integer)"%table)	
		con.execute("alter table %s alter column dessert type integer using cast(dessert as integer)"%table)	
		con.execute("alter table %s alter column yogurt type integer using cast(yogurt as integer)"%table)	
		con.execute("alter table %s alter column salad type integer using cast(salad as integer)"%table)	
		con.execute("alter table %s alter column cereal_grains type integer using cast(cereal_grains as integer)"%table)	
		con.execute("alter table %s alter column vegetable type integer using cast(vegetable as integer)"%table)	
		con.execute("alter table %s alter column snaks type integer using cast(snaks as integer)"%table)	
		con.execute("alter table %s alter column dairy type integer using cast(dairy as integer)"%table)	
		con.execute("alter table %s alter column drink type integer using cast(drink as integer)"%table)	
		con.execute("alter table %s alter column fruit type integer using cast(fruit as integer)"%table)	
		con.execute("alter table %s alter column id type integer using cast(id as integer)"%table)	
		con.execute("alter table %s alter column m5_stable type integer using cast(m5_stable as integer)"%table)	
		con.execute("alter table %s alter column m5_loss type integer using cast(m5_loss as integer)"%table)	
		con.execute("alter table %s alter column m5_stable type integer using cast(m5_stable as integer)"%table)	
		con.execute("alter table %s alter column m5_gain type integer using cast(m5_gain as integer)"%table)	
		con.execute("alter table %s alter column m1 type integer using cast(m1 as integer)"%table)	
		con.execute("alter table %s alter column m2 type integer using cast(m2 as integer)"%table)	
		con.execute("alter table %s alter column m3 type integer using cast(m3 as integer)"%table)	
		con.execute("alter table %s alter column m3 type integer using cast(m3 as integer)"%table)	
		con.execute("alter table %s alter column m4 type integer using cast(m4 as integer)"%table)
		con.execute("alter table %s add column squared_diff_weight_loss float" % table )
		con.execute("alter table %s add column squared_diff_weight_loss float" % table )
	click.secho("Data Fixed " , fg = "blue")

DATA_IMPORT_COMMAND = './pgfutter --db "%s" --port "5432" --user "%s" -pw "%s" --schema public --table %s csv %s' 

@click.command()
@click.option("--db" , prompt="Name of Database" , help="Name of Database")
@click.option("--table" , prompt="Database Table" , help="Database Table")
@click.option("--user" , prompt="Database User" , help="Database User")
@click.option("--password" , prompt=True , hide_input=True)
@click.option("--file" , prompt="file" , help="File to import from")
def hello(db , table , user , password , file):
	command = DATA_IMPORT_COMMAND % (db , user , password , table , file)
	subprocess.call(command , shell = True)
	click.echo(command)
	click.secho('Data Imported' , fg='green')
	update_table(table , url = "postgresql://%s:%s@localhost:5432/%s" % (user , password, db))



if __name__ == "__main__":
	hello()