import cx_Freeze
#setup , Executable
#from cx_Freeze import setup, Executable

cx_Freeze.setup(
	name="Maestro",
	options={},
	version="0.01",
	description="programa",
	executables=[cx_Freeze.Executable("Recolectar Datos De Entrenamiento_3.py")]
	)