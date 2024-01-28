import snowflake.connector

class tuple_with_replace():
  def __init__(self, tup):
    self.tup = tup

  def replace(self, search, replace):
    sanitized_tuple = ()
    for i in self.tup:
      if isinstance(i, str):
        sanitized_tuple += (i.replace(search, replace),)
      else:
        sanitized_tuple += (i,)
    return tuple_with_replace(sanitized_tuple)

  def __str__(self):
    return str(self.tup)

con = snowflake.connector.connect(
  user = '<username>',
  password = '<password>',
  account = '<account>',
  session_parameters = {
    'QUERY_TAG': 'EndOfMonthFinancials'
  }
)

print(con)
cur = con.cursor()
bind_variables = list()
bind_variables.append(tuple_with_replace((12, 'FURNITURE')))
bind_variables.append(tuple_with_replace((14, 'HOUSEHOLD')))
cur.execute("select c_custkey from snowflake_sample_data.tpch_sf1.customer where (c_nationkey, c_mktsegment) in (%s) and c_custkey < 500", (bind_variables,))
print("The sfqid is", cur.sfqid)
for (col1,) in cur:
  print("The result is", str(col1))
