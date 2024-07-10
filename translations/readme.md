1: extract messages ( pybabel extract -F babel.cfg -o messages.pot . )

2: initialize new languages (
  pybabel init -i messages.pot -d translations -l en
  pybabel init -i messages.pot -d translations -l ka
)

3: Note: if you want to later update the .po file after creating a new messages.pot file ( 
  pybabel update -d translations -i messages.pot -l fr 
  )

4: Compile translations: ( pybabel compile -d translations )