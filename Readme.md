This project is created as learning project
so there is no such big opportunities other
databases give.

This database works with files which means
this database don't use "СУБД" and saves everything 
like bytes in the ".txt" files



Using Example:

create database:

    my_database = Database(database_path)
    my_database.create_database()


create tables:
    
    table = Table(
        table_name,
        Col("id"),
        Col("name", default_value=None),
        Col("created_at", default_value=datetime.now,
    )
    
    my_database.create(table)


Insert:
    
    table.insert(id=1, name="Name")

Select:
    
    table.select("id").where(name="Name")

Update:
        
    table.update(id=2).where(name="Name")

Delete:

    table.delete().where(id=2)
