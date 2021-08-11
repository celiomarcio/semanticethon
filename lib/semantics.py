import re
from time import time
from datetime import datetime
from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, URIRef, XSD, OWL
from decimal import Decimal

from lib.constants import ETHON, ETHEXTRAS, SSN, DUL, GEO, SAO, CT, PROV, TL, UCUM, ID, METADATA 


from web3 import Web3, HTTPProvider

__INDEX = 'ethereum'
__SOURCE = '_source'
__ID = '_id'
__HITS = 'hits'

def __connectInfura(ethNetwork):
    if   ethNetwork == "ropsten":
        w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/"))
    elif ethNetwork == "mainnet":
        w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/"))
    elif ethNetwork == "localnode":
        w3 = Web3(HTTPProvider("http://192.168.0.23:8545"))
    else :
        w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/"))
    return w3 

def __create_graph_ethon():
    g = Graph()
    g.bind('ethon', ETHON)
    g.bind('ethextras', ETHEXTRAS)
    g.bind('owl', OWL)
    return g

def semantic_accounts(id, url, ethNetwork, output_format):

    p=re.compile('((^http(s)?\:\/\/.*)\/.*\/\w+)(\?format\=.*)?$')

    m=p.match(url)

    w3 = __connectInfura(ethNetwork)

    urlAccount = m.group(1) 

    g = __create_graph_ethon()

    account_node = URIRef(urlAccount)

    g.add((account_node, RDF.type, ETHON.Account))
        
    g.add(( account_node, ETHON.address, Literal( id, datatype=XSD.hexBinary) ))

    #balance
    g.add(( account_node, ETHEXTRAS.balance, Literal( w3.eth.get_balance("0x"+ id), datatype=XSD.integer) ))


    return g.serialize(format=output_format) 

def semantic_block(id, url, ethNetwork, output_format):
    
    p=re.compile('((^http(s)?\:\/\/.*)\/.*\/[0-9|a-z]+)(\?format\=.*)?$')

    m=p.match(url)

    w3 = __connectInfura(ethNetwork)

    if id == 'latest':
        block=w3.eth.getBlock('latest')
    else:
        block=w3.eth.getBlock(int(id))

    if block.number != 0 :
        parentBlock = m.group(2) + '/blocks/' + str(block.number-1)

    urlTransaction = m.group(2) + '/transactions'

    urlAccount = m.group(2) + '/accounts'

    urlUncles = m.group(1) + '/uncles'

    g = __create_graph_ethon()

    block_node = URIRef(m.group(2) + '/blocks/' + str(block.number) )

    g.add((block_node, RDF.type, ETHON.Block))
        
    g.add(( block_node, ETHON.number, Literal(block.number, datatype=XSD.integer) ))
   
    #blockHash = BNode()
    g.add(( block_node, ETHON.blockHash, Literal( block.hash.hex()[2:], datatype=XSD.hexBinary) ))

    if int(block.number) != 0 :
        #hasParentBlock = BNode()
        g.add(( block_node, ETHON.hasParentBlock, URIRef(parentBlock) ))

    for i in range(len(block.uncles)):
        #includesUncle = BNode()
        g.add(( block_node, ETHON.includesUncle, URIRef(  urlUncles + "/"+str(i) )  ))
        #g.add(( URIRef(  urlUncles + "/"+ str(i) ), OWL.ObjectProperty, Literal( block.uncles[i].hex()[2:], datatype=XSD.hexBinary) ))
    
    #blockNonce = BNode()
    g.add(( block_node, ETHON.blockNonce, Literal( block.nonce.hex()[2:], datatype=XSD.hexBinary) ))

    for i in range(len(block.transactions)):
        #containsTX = BNode()
        g.add(( block_node, ETHON.containsTx, URIRef( urlTransaction + "/" + block.transactions[i].hex()[2:] ) ))
        #g.add(( URIRef ( urlTransaction + "/" + str(i) ), OWL.InverseFunctionalProperty, Literal( block.transactions[i].hex()[2:], datatype=XSD.hexBinary) ))
    
    #blockLogsBloom = BNode()   
    g.add(( block_node, ETHON.blockLogsBloom, Literal( block.logsBloom.hex()[2:], datatype=XSD.hexBinary)  ))
    #hasBeneficiary
    g.add(( block_node, ETHON.hasBeneficiary, URIRef( urlAccount + "/" + block.miner[2:])  ))
    #blockDifficulty = BNode()
    g.add(( block_node, ETHON.blockDifficulty, Literal( block.difficulty, datatype=XSD.integer) ))
    #blockExtraData
    g.add(( block_node, ETHON.blockExtraData, Literal( block.extraData.hex()[2:], datatype=XSD.hexBinary)  ))
    #miner
    g.add(( block_node, ETHEXTRAS.miner, URIRef( urlAccount + "/" + block.miner[2:])  ))
    #blockGasUsed
    g.add(( block_node, ETHON.blockGasUsed, Literal( block.gasUsed, datatype=XSD.integer) ))
    #blockGasLimit
    g.add(( block_node, ETHON.blockGasLimit, Literal( block.gasLimit, datatype=XSD.integer) ))
    #blockMixHash
    g.add(( block_node, ETHON.blockMixHash, Literal( block.mixHash.hex()[2:], datatype=XSD.hexBinary)  ))
    #receiptRoot
    g.add(( block_node, ETHEXTRAS.receiptsRoot, Literal( block.receiptsRoot.hex()[2:], datatype=XSD.hexBinary)  ))
    #blockSize
    g.add(( block_node, ETHON.blockSize, Literal( block.size, datatype=XSD.integer) ))
    #stateRoot
    g.add(( block_node, ETHEXTRAS.stateRoot, Literal( block.stateRoot.hex()[2:], datatype=XSD.hexBinary) ))
    #transactionRoot
    g.add(( block_node, ETHEXTRAS.transactionsRoot, Literal( block.transactionsRoot.hex()[2:], datatype=XSD.hexBinary) ))
    #mixHash
    g.add(( block_node, ETHEXTRAS.mixHash, Literal( block.mixHash.hex()[2:], datatype=XSD.hexBinary) ))

    if int(block.number) != 0 :
        #blockCreationTime
        g.add(( block_node, ETHON.blockCreationTime, Literal( datetime.fromtimestamp(block.timestamp).isoformat(), datatype=XSD.dateTime) ))
    
    return g.serialize(format=output_format)

def semantic_uncle(id, uncle_id, url, ethNetwork, output_format):
    
    p=re.compile('(((^http(s)?\:\/\/.*\/.*)\/.*\/.*)\/.*/[0-9]+)(\?format\=.*)?$')

    m=p.match(url)

    w3 = __connectInfura(ethNetwork)

    uncle=w3.eth.get_uncle_by_block(int(id), int(uncle_id))

    parentBlock = re.sub(r"\b{}\b".format(id), str(int(id)-1), m.group(2))

    urlAccount = m.group(3) + '/accounts'

    g = __create_graph_ethon()

    uncle_node = URIRef(m.group(1))

    g.add((uncle_node, RDF.type, ETHON.Uncle))
        
    #totalBlockDifficulty
    g.add(( uncle_node, ETHON.totalBlockDifficulty, Literal( int(uncle.difficulty, 16), datatype=XSD.integer) ))
    #number
    g.add(( uncle_node, ETHON.number, Literal(int(uncle.number, 16), datatype=XSD.integer) ))
    #blockExtraData
    g.add(( uncle_node, ETHON.blockExtraData, Literal( uncle.extraData[2:], datatype=XSD.hexBinary)  ))
    #blockGasLimit
    g.add(( uncle_node, ETHON.blockGasLimit, Literal( int(uncle.gasLimit,16), datatype=XSD.integer) ))
    #blockGasUsed
    g.add(( uncle_node, ETHON.blockGasUsed, Literal( int(uncle.gasUsed,16), datatype=XSD.integer) ))
    #blockHash 
    g.add(( uncle_node, ETHON.blockHash, Literal( uncle.hash[2:], datatype=XSD.hexBinary) ))
    #blockLogsBloom    
    g.add(( uncle_node, ETHON.blockLogsBloom, Literal( uncle.logsBloom[2:], datatype=XSD.hexBinary)  ))
    #hasBeneficiary
    g.add(( uncle_node, ETHON.hasBeneficiary, URIRef( urlAccount + "/" + uncle.miner[2:])  ))
    #blockMixHash
    g.add(( uncle_node, ETHON.blockMixHash, Literal( uncle.mixHash[2:], datatype=XSD.hexBinary)  ))
    #blockNonce 
    g.add(( uncle_node, ETHON.blockNonce, Literal( uncle.nonce[2:], datatype=XSD.hexBinary) ))
    #hasParentBlock
    g.add(( uncle_node, ETHON.hasParentBlock, URIRef(parentBlock) ))
    #hasReceiptsTrie
    g.add(( uncle_node, ETHON.hasReceiptsTrie, Literal( uncle.receiptsRoot[2:], datatype=XSD.hexBinary)  ))
    #blockSize
    g.add(( uncle_node, ETHON.blockSize, Literal( int(uncle.size,16), datatype=XSD.integer) ))
    #createsPostBlockState
    g.add(( uncle_node, ETHON.createsPostBlockState, Literal( uncle.stateRoot[2:], datatype=XSD.hexBinary) ))
    #blockCreationTime
    g.add(( uncle_node, ETHON.blockCreationTime, Literal( datetime.fromtimestamp(int(uncle.timestamp,16)).isoformat(), datatype=XSD.dateTime) ))

    return g.serialize(format=output_format)

def semantic_transaction(id, url, ethNetwork, output_format):
    
    p=re.compile('((^http(s)?\:\/\/.*)\/.*\/[0-9|a-z]+)(\?format\=.*)?$')

    m=p.match(url)

    w3 = __connectInfura(ethNetwork)

    transaction=w3.eth.get_transaction("0x"+ id)

    urlBlock = m.group(2) + '/blocks'

    urlAccount = m.group(2) + '/accounts'

    urlReceipt = m.group(2) + "/receipts"

    g = __create_graph_ethon()

    transaction_node = URIRef(m.group(1))

    g.add((transaction_node, RDF.type, ETHON.Tx))

    #blockNumber
    g.add(( transaction_node, ETHEXTRAS.blockNumber, Literal( transaction.blockNumber, datatype=XSD.integer)  )) 
    #inBlock
    g.add(( transaction_node, ETHEXTRAS.inBlock, URIRef( urlBlock + "/" + str(transaction.blockNumber) )  ))
    #from
    g.add(( transaction_node, URIRef(ETHON + "from"), URIRef( urlAccount + "/" + getattr(transaction,'from')[2:] )  ))
    #txGasUsed
    g.add(( transaction_node, ETHON.txGasUsed, Literal( transaction.gas, datatype=XSD.integer) ))
    #txGasPrice
    g.add(( transaction_node, ETHON.txGasPrice, Literal( transaction.gasPrice, datatype=XSD.integer) ))
    #txHash
    g.add(( transaction_node, ETHON.txHash, Literal( transaction.hash.hex()[2:], datatype=XSD.hexBinary) ))
    #txNonce
    g.add(( transaction_node, ETHON.txNonce, Literal( transaction.nonce, datatype=XSD.integer) ))
    #txR
    g.add(( transaction_node, ETHON.txR, Literal( transaction.r.hex()[2:], datatype=XSD.hexBinary) ))
    #txS
    g.add(( transaction_node, ETHON.txS, Literal( transaction.s.hex()[2:], datatype=XSD.hexBinary) ))
    #txIndex
    g.add(( transaction_node, ETHON.txIndex, Literal( transaction.transactionIndex, datatype=XSD.integer) ))
    #to if None is a Contract Creation
    if transaction.to:
        g.add(( transaction_node, ETHON.to, URIRef( urlAccount + "/" + transaction.to[2:]) ))
    else:
        g.add(( transaction_node, ETHON.to, Literal( urlAccount + "/" + "0" ) ))
    #msgPayload
    g.add(( transaction_node, ETHON.msgPayload, Literal( transaction.input[2:], datatype=XSD.hexBinary) ))
    #value
    g.add(( transaction_node, ETHON.value, Literal( transaction.value, datatype=XSD.integer ) ))
    #hasReceipt
    g.add((transaction_node, ETHON.hasReceipt, URIRef( urlReceipt + "/" + id ) ))
  
    return g.serialize(format=output_format)

def semantic_receipt(transaction, url, ethNetwork, output_format):
    
    p=re.compile('((^http(s)?\:\/\/.*)\/.*\/[0-9|a-z]+)(\?format\=.*)?$')

    m=p.match(url)

    w3 = __connectInfura(ethNetwork)

    receipt=w3.eth.get_transaction_receipt("0x"+ transaction)

    g = __create_graph_ethon()

    receipt_node = URIRef(m.group(1))

    urlBlock = m.group(2) + '/blocks'

    urlAccount = m.group(2) + '/accounts'

    urlContract = m.group(2) + '/contracts'

    g.add((receipt_node, RDF.type, ETHON.TxReceipt))
    #blockHash
    g.add(( receipt_node, ETHEXTRAS.blockHash, Literal( receipt.blockHash.hex()[2:], datatype=XSD.hexBinary) ))
    
    if receipt.contractAddress:
        #contract
        g.add(( receipt_node, ETHEXTRAS.contract, URIRef( urlContract +"/"+ receipt.contractAddress[2:] ) ))
    #cumulativeGasUsed
    g.add(( receipt_node, ETHEXTRAS.cumulativeGasUsed, Literal( receipt.cumulativeGasUsed, datatype=XSD.integer) ))
    #gasUsed
    g.add(( receipt_node, ETHEXTRAS.gasUsed, Literal( receipt.gasUsed, datatype=XSD.integer)  ))
    #from
    g.add(( receipt_node, URIRef(ETHEXTRAS + "from"), URIRef( urlAccount + "/" + getattr(receipt,'from')[2:] )  ))
    #logsBloom    
    g.add(( receipt_node, ETHEXTRAS.logsBloom, Literal( receipt.logsBloom.hex()[2:], datatype=XSD.hexBinary)  ))
    #inBlock
    g.add(( receipt_node, ETHEXTRAS.inBlock, URIRef( urlBlock + "/" + str(receipt.blockNumber) )  ))
    #to if None is a Contract Creation
    if receipt.to:
        g.add(( receipt_node, ETHON.to, URIRef( urlAccount + "/" + receipt.to[2:]) ))
    else:
        g.add(( receipt_node, ETHON.to, Literal( urlAccount + "/" + "0" ) ))
    #transactionHash
    g.add(( receipt_node, ETHEXTRAS.transactionHash, Literal( receipt.transactionHash.hex()[2:], datatype=XSD.hexBinary) ))
    #transactionIndex
    g.add(( receipt_node, ETHEXTRAS.transactionIndex, Literal( receipt.transactionIndex, datatype=XSD.integer)  ))
    #type
    g.add(( receipt_node, ETHEXTRAS.type, Literal( receipt.type[2:], datatype=XSD.hexBinary) ))
    


    return g.serialize(format=output_format)

def semantic_contracts(id, url, ethNetwork, output_format):

    p=re.compile('((^http(s)?\:\/\/.*)\/.*\/\w+)(\?format\=.*)?$')

    m=p.match(url)

    w3 = __connectInfura(ethNetwork)

    urlContract = m.group(1) 

    g = __create_graph_ethon()

    contract_node = URIRef(urlContract)

    g.add((contract_node, RDF.type, ETHON.ContractAccount))
        
    g.add(( contract_node, ETHON.address, Literal( id, datatype=XSD.hexBinary) ))

    #balance
    g.add(( contract_node, ETHEXTRAS.balance, Literal( w3.eth.get_balance("0x"+ id), datatype=XSD.integer) ))


    return g.serialize(format=output_format) 

if __name__ == '__main__':
    print("hello")
                                 