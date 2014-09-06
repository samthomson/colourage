import rethinkdb as r



if __name__ == '__main__':

	conn = r.connect(host = 'localhost', db = 'colourage')

	r.db("colourage")

	i_r = 152
	i_g = 64
	i_b = 89

	i_offset = 20



	result = r.table('seed_colours').filter(
		(r.row["red"] >= i_r-i_offset) & (r.row["red"] <= i_r+i_offset) &
		(r.row["green"] >= i_g-i_offset) & (r.row["green"] <= i_g+i_offset) &
		(r.row["blue"] >= i_b-i_offset) & (r.row["blue"] <= i_b+i_offset)
		).limit(1).run(conn)
	for image in result:
		print image["file"]
	"""
	for c in r.table('seed_colours').filter(
		(r.row["red"] >= i_r-10) & (r.row["red"] <= i_r+10) &
		(r.row["green"] >= i_g-10) & (r.row["green"] <= i_g+10) &
		(r.row["blue"] >= i_b-10) & (r.row["blue"] <= i_b+10)
		).limit(1).run(conn):
		print c

	"""