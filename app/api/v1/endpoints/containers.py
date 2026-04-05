from fastapi import APIRouter, Body
from app.models.schema import contrainerInfo, contMetrics, contID
from app.core.database import *
from app.core.utils import *
from typing import List

router = APIRouter(prefix="/containers", tags=["Containers"])

@router.post("/sendContList/")
async def sendContList(containers: List[contrainerInfo] = Body(...)):
    # Проверку на дубликаты
    for container in containers:
        if not Container.select().where(Container.ID == container.id).exists():
            host = Host.select().where(Host.hostname == container.hostname).first()
            cont = Container.create(
                ID=container.id,
                image=container.image,
                name=container.name,
                hostID=host.id
            )
            cont.save()
    return {"code": "success"}

@router.post("/sendContainerStats/")
async def sendMetrics(metrics: List[contMetrics] = Body(...)):
    for stat in metrics:
        if Container.select().where(Container.ID == stat.contID).exists():
            contain = Container.get(Container.ID == stat.contID)
            if(contain.isActive):
                cont = ContStat.create(
                    contID=stat.contID,
                    lastUpdate=stat.lastUpdate,
                    loadRAM=round(stat.loadRAM,3),
                    loadCPU=round(stat.loadCPU,3),
                    status=stat.status
                )
                cont.save()
    return {"code": "success"}

@router.get("/getContList/")
async def getContList():
    query = Container.select()
    result = []
    for container in query:
        result.append({"contID": container.ID, "image": container.image, "name": container.name, "hostID": container.hostID})
    return result

@router.get("/getContView/")
async def getContView():
    query = ContView.select()
    result = []
    for container in query:
        result.append({"contID": container.ContID,
                       "ContName": container.ContName,
                       "HostID": container.HostID,
                       "hostname": container.hostname,
                       "status": container.ContainerStatus,
                       "isActive": container.isActive,
                       "loadCPU": container.loadCPU,
                       "loadRAM": container.loadRAM
                       })
    return result

@router.get("/getContStat/")
async def getContView(contID: str):
    query = ContStatView.select()
    result = []
    for stat in query:
        result.append({"contID": stat.ContID,
                       "lastUpdate": stat.lastUpdate,
                       "loadCPU": stat.loadCPU,
                       "loadRAM": stat.loadRAM,
                       "status": stat.status,
                       })
    return result

@router.delete("/deleteContainer/")
async def deleteContainer(container: contID = Body(...)):
    Container.update({"isActive": False}).where(Container.ID == container.contID).execute()
    return {"status": "success"}

@router.put("/restoreContainer/")
async def restoreContainer(container: contID):
    Container.update({"isActive": True}).where(Container.ID == container.contID).execute()
    return {"status": "success"}

@router.get("/getUML/")
async def getUML():
    query = ContView.select()
    classes = []
    for container in query:
        classes.append({"name": container.ContName,
                       "loadCPU": container.loadCPU,
                       "loadRAM": container.loadRAM
                       })
    relations = []
    query = ConnView.select()
    for net in query:
        relations.append({"from": net.sourceID,
                       "to": net.targetID,
                       "type": "network"
                       })
    
    return generate_plantuml(classes,relations)