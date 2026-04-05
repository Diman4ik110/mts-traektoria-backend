from fastapi import APIRouter, Body
from app.models.schema import networkList, networkConnection, networkStat, connID
from app.core.database import *
from typing import List

router = APIRouter(prefix="/netinfo", tags=["Network"])

@router.post("/sendNetList/")
async def sendNetList(network: networkList = Body(...)):
    # Проверку на дубликаты
    if not Network.select().where(Network.ID == network.netID).exists():
        net = Network.create(
            ID=network.netID,
            name=network.name
        )
        net.save()
    return {"code": "success"}

@router.post("/sendNetData/")
async def sendNetData():
    # Проверку на дубликаты
    
    return {"code": "success"}

@router.post("/sendNetConnection/")
async def sendNetConnection(netConnectList: List[networkConnection] = Body(...)):
    # Проверку на дубликаты
    for connect in netConnectList:
        if not NetworkConn.select().where((NetworkConn.networkID == connect.netID) & (NetworkConn.containerID == connect.contID)).exists():
            netConnect = NetworkConn.create(
                containerID=connect.contID,
                networkID=connect.netID
            )
            netConnect.save()
    return {"code": "success"}

@router.get("/getNetList/")
async def getNetList():
    query = Network.select()
    result = []
    for item in query:
        result.append({"netID": item.ID, "name": item.name})
    return result

@router.get("/getNetConnection/")
async def getNetConnection():
    query = NetworkConn.select()
    result = []
    for connection in query:
        result.append({"contID": connection.containerID, "netID": connection.networkID})
    return result

@router.get("/getLinksView/")
async def getLinksView():
    query = ConnView.select()
    result = []
    for link in query:
        result.append({"sourceID": link.sourceID,
                       "targetID": link.targetID,
                       "netID": link.netID,
                       "networkName": link.networkName,
                       "isActive": link.isActive
                       })
    return result

@router.post("/sendNetworkStat/")
async def sendNetworkStat(netStat: networkStat = Body(...)):
    if not Container.select().where(Container.ID == netStat.contID).exists():
        # Проверку на дубликаты
        netStat = NetworkStat.create(
            lastUpdate=netStat.lastUpdate,
            contID=netStat.contID,
            rxSpeed=netStat.rxSpeed,
            txSpeed=netStat.txSpeed,
            rxBytes=netStat.rxBytes,
            txBytes=netStat.txBytes
        )
        netStat.save()
        return {"code": "success"}
    else:
        contain = Container.get(Container.ID == netStat.contID)
        if(contain.isActive):
            # Проверку на дубликаты
            netStat = NetworkStat.create(
                lastUpdate=netStat.lastUpdate,
                contID=netStat.contID,
                rxSpeed=netStat.rxSpeed,
                txSpeed=netStat.txSpeed,
                rxBytes=netStat.rxBytes,
                txBytes=netStat.txBytes
            )
            netStat.save()
            return {"code": "success"}

@router.get("/getNetStatView/")
async def getNetStatView():
    query = NetworkStatView.select()
    result = []
    # Проверку на дубликаты
    for netstat in query:
         result.append({
                "contID": netstat.contID,
                "rxSpeed": netstat.rxSpeed,
                "txSpeed": netstat.txSpeed,
                "rxBytes": netstat.rxBytes,
                "txBytes": netstat.txBytes
            })
    return result
@router.delete("/deleteConnection/")
async def deleteConnection(netID: connID):
    Network.update({"isActive": False}).where(Network.ID == netID.connID).execute()
    return {"status": "success"}

@router.put("/restoreConnection")
async def restoreConnection(netID: connID):
    Network.update({"isActive": True}).where(Network.ID == netID.connID).execute()
    return {"status": "success"}