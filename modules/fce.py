from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from modules import models, schemas
from modules.hashing import Hash
import json

#filePath = '/home/lolek/projects/myAPI/static/data.json'
filePath = 'static/data.json'

# ------------- Reload data from json file ------------------------------
def reloadData():
    with open(filePath) as json_file:
        data = json.load(json_file)
    return data

# ------------- Write data to json file ------------------------------
def writeData(dataToWrite):
    with open(filePath,'w', encoding='utf-8') as outfile:
        json.dump(dataToWrite, outfile, ensure_ascii=False, indent=4)

# ------------- Update DB from json file ------------------------------
def updateDB(db: Session):    
    items = db.query(models.App).all()
    
    if items:
        db.query(models.App).delete(synchronize_session=False)
        db.commit()
        
    
    data = reloadData()

    for item in data:
        # Convert List of strings to string
        if type(item['LastCommands']) is not list:         
            if item['LastCommands'] != None and item['LastCommands'] != "":
                item['LastCommands'] = [str(c) for c in item['LastCommands']]
            else:
                item['LastCommands'] = []
        itemOBJ = schemas.AppItem(**item)

        if itemOBJ.LastCommands: 
            lc_str = ';'.join([str(lc) for lc in itemOBJ.LastCommands])
        else:
            lc_str = ""
                
        new_item = models.App(
            ID = itemOBJ.ID, 
            Server = itemOBJ.Server,
            Name = itemOBJ.Name, 
            Pos = itemOBJ.Pos, 
            Path = itemOBJ.Path, 
            Port = itemOBJ.Port,
            Enabled = itemOBJ.Enabled,
            Required = itemOBJ.Required,
            LastCommands = lc_str,   
            Running = itemOBJ.Running,
            Pid = itemOBJ.Pid,
            Material = itemOBJ.Material,
            Order = itemOBJ.Order,
            Message = itemOBJ.Message
            )

        
        # Write item to DB
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        

# ===================================== Apps =====================================

# ------------------------------------ GET ALL -----------------------------------------------#
def get_all(name: str, db: Session):    
    if name == None:
        items = db.query(models.App).all()
    else:
        items = db.query(models.App).filter(models.App.Name == name).all()        
    
    if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with name {name} not found!")

    for item in items:
            if item.LastCommands: 
                lc_list = item.LastCommands.split(';')
            else:
                lc_list = []
            
            item.LastCommands = lc_list            
    return items

# ------------------------------------ GET ID -----------------------------------------------#
def show(id: int, db: Session):
    item = db.query(models.App).filter(models.App.ID == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item ID {id} not found!")

    if item.LastCommands: 
        lc_list = item.LastCommands.split(';')
    else:
        lc_list = []
    
    item.LastCommands = lc_list 

    return item

# ------------------------------------ POST -----------------------------------------------#
def create(id: int, item: schemas.AppItem, db: Session):
    data = reloadData()
    item_dict = item.dict()
        
    # Convert List of strings to string
    if item.LastCommands: 
        lc_str = ';'.join([str(lc) for lc in item.LastCommands])
    else:
        lc_str = ""
    
    for i in data:
        if i["ID"] == id:
            raise HTTPException(status_code=400, detail=f"Item ID {id} already exists!")

    # Write to file
    item_dict.update({"ID": id})
    data.append(item_dict)
    writeData(data)

    # Write to DB
    new_item = models.App(
        ID = id, 
        Server = item.Server,
        Name = item.Name, 
        Pos = item.Pos, 
        Path = item.Path, 
        Port = item.Port,
        Enabled = item.Enabled,
        Required = item.Required,
        LastCommands = lc_str,   
        Running = item.Running,
        Pid = item.Pid,
        Material = item.Material,
        Order = item.Order,
        Message = item.Message
        )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return data[-1]
    #return new_item

# ------------------------------------ PUT -----------------------------------------------#
def update(id: int, item: schemas.AppItem, db: Session):
    data = reloadData()
    item_dict = item.dict()

    i = db.query(models.App).filter(models.App.ID == id)

    if not i.first():
        raise HTTPException(status_code=404, detail=f"Item ID {id} doesn't exist!")
    
    lc = item.LastCommands

    # Convert List of strings to string
    if item.LastCommands: 
        lc_str = ';'.join([str(lc) for lc in item.LastCommands])
    else:
        lc_str = ""

    item.LastCommands = lc_str
    updated_item = item.dict(exclude_unset=True)    
    

    # Write to DB
    i.update(jsonable_encoder(updated_item))
    db.commit()

    # Write to file    
    for app in data:
        if app["ID"] == id:
            updated_item['LastCommands'] = lc
            app.update(updated_item)

    writeData(data)

    item.LastCommands = lc
    return item

# ------------------------------------ DELETE -----------------------------------------------#
def destroy(data, id: int, db: Session):
    item = db.query(models.App).filter(models.App.ID == id)    
    if not item.first():        
        raise HTTPException(status_code=404, detail=f"Item ID {id} doesn't exist!")
    
    item.delete(synchronize_session=False)
    db.commit()

    data = reloadData()

    for i in data:
        if i["ID"] == id:
            data.remove(i)
            writeData(data)
            raise HTTPException(status_code=200, detail=f"Item ID {id} deleted!")

    raise HTTPException(status_code=404, detail=f"Item ID {id} doesn't exist!")

# ==================================== User =====================================

# ------------------------------------ POST -----------------------------------------------#
def create_user(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ------------------------------------ GET ID -----------------------------------------------#
def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} doesn't exist!")
    return user
