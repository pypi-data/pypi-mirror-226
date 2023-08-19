from pathlib import Path

serve_path = str(Path(__file__).with_name("vue3").resolve())
serve = {"__trame_quasar": serve_path }
scripts = [
    "__trame_quasar/1.js",
]
styles = [
    "__trame_quasar/2.css",
    "__trame_quasar/3.css",
]
vue_use = [
    "Quasar",
]
