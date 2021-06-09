import cx_Oracle
import xml.etree.ElementTree as ET

user = "login"
password = "password"

options = {
    1: "Export",
    2: "Import"
}

for key_options, value_options in options.items():
    print(f'{key_options}: {value_options}')

print()

while True:
    try:
        chosen_option = int(input("Wybierz opcje:"))
        if chosen_option < 1 or chosen_option > 2:
            print("Musisz podać cyfre 1 lub 2")
        else:
            break
    except ValueError:
        print("Musisz podać cyfre")

print()
print(options[chosen_option])
print()

try:
    connection = cx_Oracle.connect(user, password, 'myservice')
except Exception as err:
    print('Error while creating the connection', err)
else:
    try:
        cursor = connection.cursor()
    except Exception as err:
        print('Error while inserting the data ', err)
    else:
        if chosen_option == 1: # EXPORT
            file = open('file.xml', 'w')
            query = """SELECT * FROM uczen"""
            cursor.execute(query)
            rows = cursor.fetchall()
            file.write('<?xml version="1.0"?>\n')
            file.write('<s97629>\n')
            for row in rows:
                file.write('    <uczen>\n')
                file.write('        <id_uczen>' + str(row[0]) + '</id_uczen>\n')
                file.write('        <imie>' + str(row[1]) +'</imie>\n')
                file.write('        <nazwisko>' + str(row[2]) +'</nazwisko>\n')
                file.write('        <data_urodzenia>' + str(row[3]) +'</data_urodzenia>\n')
                file.write('        <pesel>' + str(row[4]) +'</pesel>\n')
                file.write('        <email>' + str(row[5]) +'</email>\n')
                file.write('        <nr_tel>' + str(row[6]) +'</nr_tel>\n')
                file.write('    </uczen>\n')
            file.write('</s97629>\n')
            file.close()
            print("EXPORT COMPLETE!")

            
        elif chosen_option == 2:  # IMPORT
            tree = ET.parse('file.xml')
            emp = tree.findall('uczen')
            
            for ep in emp:
                id_uczen = ep.find('id_uczen').text
                imie = ep.find('imie').text
                nazwisko = ep.find('nazwisko').text
                data_urodzenia = ep.find('data_urodzenia').text
                pesel = ep.find('pesel').text
                email = ep.find('email').text
                nr_tel = ep.find('nr_tel').text

                query = """UPDATE uczen SET id_uczen = :1, imie = :2, nazwisko = :3, data_urodzenia = :4, pesel = :5, email = :6, nr_tel = :7 
                           WHERE id_uczen = :1"""
                cursor.execute(query,(id_uczen,imie,nazwisko,data_urodzenia,pesel,email,nr_tel))
            connection.commit()
            print("IMPORT COMPLETE!")

        print('DONE!')
        connection.commit()
finally:
    cursor.close()
    connection.close()
