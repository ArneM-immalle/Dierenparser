from dataclasses import dataclass
import sqlite3, os


if (os.path.exists('dieren.db')):
    os.remove('dieren.db')
conn = sqlite3.connect('dieren.db')
c = conn.cursor()
c.execute('''CREATE TABLE dieren (naam text, soort text, aantalPoten integer, kleur text, geluid text)''')


@dataclass
class Dier:
    naam: str
    soort: str
    aantalPoten: int
    kleur: str
    geluid: str

    def insertSQL(self):
        c.execute("""INSERT INTO dieren(naam, soort, aantalPoten, kleur, geluid) 
               VALUES (?,?,?,?,?);""", (self.naam, self.soort, self.aantalPoten, self.kleur, self.geluid))

        # Save (commit) the changes
        conn.commit()

def getData(manier):
    if manier == "naam":
        return c.execute("SELECT * FROM dieren ORDER BY naam ASC")
    else:
        return c.execute("SELECT * FROM dieren ORDER BY soort ASC")


def parse_line(line : str) -> Dier:
    naam, soort, aantalpoten, kleur, geluid = line.split(' - ')
    d = Dier(naam, soort, int(aantalpoten), kleur, geluid)
    return d


def parse_text(str : str) -> [Dier]:
    dieren = []
    for line in str.splitlines():
        d = parse_line(line)
        dieren.append(d)
    return dieren


if __name__ == '__main__':
    dieren = []
    with open('dieren.txt', 'r') as f:
        dieren = parse_text(f.read())

    for dier in dieren:
        dier.insertSQL()
        print(dier)
    
    for dier in getData("naam"):
        print(dier)
    
    for dier in getData("soort"):
        print(dier)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()