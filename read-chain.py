import subprocess
import json
from string import Template
import pyodbc
import datetime

# Go get a bearer token from the JHipster UI, under Administration/API use "Try it out" for a block or a Tx and
# grab the token from there. They are transient, so get a new one each session.
bearer = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImF1dGgiOiJST0xFX0FETUlOLFJPTEVfVVNFUiIsImV4cCI6MTU0NDU4NTg1N30.uvEbGN0afYUPviCAFNGcRV_GWZw4RAQETnSE_NjMogNU64B-whLREbecW6zF75rRuua3gtuOx5KXTVt5n-dkyQ"

veruscmd = '/home/virtualsoundnw/Agama-linux-x64/resources/app/assets/bin/linux64/verusd/verus'

blocks = 'blocks'

createblocktable = '''
CREATE TABLE IF NOT EXISTS block (
  height bigint(20) NOT NULL,
  hash varchar(255) NOT NULL,
  confirmation bigint(20) DEFAULT NULL,
  version bigint(20) DEFAULT NULL,
  merkleroot varchar(255) DEFAULT NULL,
  segid bigint(20) DEFAULT NULL,
  finalsaplingroot varchar(255) DEFAULT NULL,
  time datetime,
  nonce varchar(255) DEFAULT NULL,
  solution varchar(4096) DEFAULT NULL,
  bits varchar(255) DEFAULT NULL,
  difficulty double DEFAULT NULL,
  chainwork varchar(255) DEFAULT NULL,
  anchor varchar(255) DEFAULT NULL,
  blocktype varchar(255) DEFAULT NULL,
  previousblockhash varchar(255) DEFAULT NULL,
  nextblockhash varchar(255) DEFAULT NULL,
  sproutmonitored bigint(20) DEFAULT NULL,
  sproutchainvalue double DEFAULT NULL,
  sproutchainvaluezat bigint(20) DEFAULT NULL,
  sproutvaluedelta double DEFAULT NULL,
  sproutvaluedeltazat bigint(20) DEFAULT NULL,
  saplingmonitored bigint(20) DEFAULT NULL,
  saplingchainvalue double DEFAULT NULL,
  saplingchainvaluezat bigint(20) DEFAULT NULL,
  saplingvaluedelta double DEFAULT NULL,
  saplingvaluedeltazat bigint(20) DEFAULT NULL,
  size bigint(20) NOT NULL,
  PRIMARY KEY (height)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
'''

createtxtable = '''
CREATE TABLE IF NOT EXISTS tx (
  height bigint(20) NOT NULL,
  tx varchar(64) NOT NULL,
  PRIMARY KEY (height, tx),
  CONSTRAINT fk_tx_height FOREIGN KEY (height) REFERENCES block (height)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
'''
dropblocktable = '''DROP TABLE block;'''
droptxtable = '''DROP TABLE tx;'''

cnxn = pyodbc.connect('DRIVER={mySQL};SERVER=127.0.0.1;DATABASE=verus;UID=beamit;PWD=Filipino10')
cursor = cnxn.cursor()


def textdict2dict(textdict):
    result = textdict.replace("\n", "").replace("\t", "")
    resultdict = json.loads(result)
    return resultdict


def createtables(curs, conn):
    curs.execute(createblocktable)
    curs.execute(createtxtable)
    conn.commit()


def droptables(curs, conn):
    curs.execute(droptxtable)
    curs.execute(dropblocktable)
    conn.commit()


def getmininginfo():
    result = subprocess.check_output([veruscmd, 'getmininginfo'])
    return textdict2dict(result)


def getblockcount():
    miningdict = getmininginfo()
    return miningdict[blocks]


def getblock(i):
    result = subprocess.check_output([veruscmd, 'getblock', str(i)])
    #print "getblock() result: " + result
    return textdict2dict(result)


def dbblock(block, curs, conn):
    curs.execute(block)
    conn.commit()


def dbtx(tx, curs, conn):
    curs.execute(tx)
    conn.commit()


def setpools(block, blockdict):

    if block["valuePools"][0]["id"] == "sprout":
        if block["valuePools"][0]["chainValue"] == 0:
            blockdict["saplingchainValue"] = 0
        else:
            blockdict["saplingchainValue"] = block["valuePools"][0]["chainValue"]
        blockdict["saplingchainValueZat"] = block["valuePools"][0]["chainValueZat"]

        if block["valuePools"][0]["valueDelta"] == 0:
            blockdict["saplingvalueDelta"] = 0
        else:
            blockdict["saplingvalueDelta"] = block["valuePools"][0]["valueDelta"]
        blockdict["saplingvalueDeltaZat"] = block["valuePools"][0]["valueDeltaZat"]

        if block["valuePools"][0]["monitored"]:
            blockdict["saplingMonitored"] = -1
        else:
            blockdict["saplingMonitored"] = 0

        if block["valuePools"][1]["chainValue"] == 0:
            blockdict["sproutchainValue"] = 0
        else:
            blockdict["sproutchainValue"] = block["valuePools"][1]["chainValue"]
        blockdict["sproutchainValueZat"] = block["valuePools"][1]["chainValueZat"]

        if block["valuePools"][1]["valueDelta"] == 0:
            blockdict["sproutvalueDelta"] = 0
        else:
            blockdict["sproutvalueDelta"] = block["valuePools"][1]["valueDelta"]
        blockdict["sproutvalueDeltaZat"] = block["valuePools"][1]["valueDeltaZat"]

        if block["valuePools"][1]["monitored"]:
            blockdict["sproutMonitored"] = -1
        else:
            blockdict["sproutMonitored"] = 0
    else:
        if block["valuePools"][1]["chainValue"] == 0:
            blockdict["saplingchainValue"] = 0
        else:
            blockdict["saplingchainValue"] = block["valuePools"][1]["chainValue"]
        blockdict["saplingchainValueZat"] = block["valuePools"][1]["chainValueZat"]

        if block["valuePools"][1]["valueDelta"] == 0:
            blockdict["saplingvalueDelta"] = 0
        else:
            blockdict["saplingvalueDelta"] = block["valuePools"][1]["valueDelta"]
        blockdict["saplingvalueDeltaZat"] = block["valuePools"][1]["valueDeltaZat"]

        if block["valuePools"][1]["monitored"]:
            blockdict["saplingMonitored"] = -1
        else:
            blockdict["saplingMonitored"] = 0

        if block["valuePools"][0]["chainValue"] == 0:
            blockdict["sproutchainValue"] = 0
        else:
            blockdict["sproutchainValue"] = block["valuePools"][0]["chainValue"]
        blockdict["sproutchainValueZat"] = block["valuePools"][0]["chainValueZat"]

        if block["valuePools"][0]["valueDelta"] == 0:
            blockdict["sproutvalueDelta"] = 0
        else:
            blockdict["sproutvalueDelta"] = block["valuePools"][0]["valueDelta"]
        blockdict["sproutvalueDeltaZat"] = block["valuePools"][0]["valueDeltaZat"]

        if block["valuePools"][0]["monitored"]:
            blockdict["sproutMonitored"] = -1
        else:
            blockdict["sproutMonitored"] = 0

    return blockdict

def main():
    # open the file
    sqlfilein = open('/home/virtualsoundnw/PycharmProjects/vrscdb/sql-block.template')

    # read it & close it
    sqltemplate = Template(sqlfilein.read())
    sqlfilein.close()

    # repeat as needed
    sqlfileNoPrevious = open('/home/virtualsoundnw/PycharmProjects/vrscdb/sql-block-no-previous.template')
    sqltemplateNoPrevious = Template(sqlfileNoPrevious.read())
    sqlfileNoPrevious.close()

    # as
    sqlfileNoNext = open('/home/virtualsoundnw/PycharmProjects/vrscdb/sql-block-no-next.template')
    sqltemplateNoNext = Template(sqlfileNoNext.read())
    sqlfileNoNext.close()

    # needed
    sqlfileTx = open('/home/virtualsoundnw/PycharmProjects/vrscdb/sql-tx.template')
    sqltemplateTx = Template(sqlfileTx.read())
    sqlfileTx.close()

    droptables(cursor, cnxn)
    createtables(cursor, cnxn)

    # templates set, what's the current block height?
    blocks = getblockcount()
    print "Current block height is " + str(blocks)

    # Missing 0, unfortunately
    i = 0
    # should be i < blocks except it is already a quarter million
    # So when testing use the small version here:
    #while i < 2:
    while i < blocks:
        nxtTemplate = sqltemplate
        block = getblock(i)
        blockdict = {
            "anchor": block["anchor"],
            "bits": block["bits"],
            "blocktype": block["blocktype"].upper(),
            "chainwork": block["chainwork"],
            "confirmation": block["confirmations"],
            "difficulty": block["difficulty"],
            "finalsaplingroot": block["finalsaplingroot"],
            "hash": block["hash"],
            "height": block["height"],
            "merkleroot": block["merkleroot"],
            "nonce": block["nonce"],
            "segid": block["segid"],
            "size": block["size"],
            "solution": block["solution"],
            "time": datetime.datetime.fromtimestamp(block["time"]).strftime("%Y-%m-%d %H:%M:%S"),
            "tx": block["tx"],
            "version": block["version"]
        }

        if "nextblockhash" in block:
            blockdict["nextblockhash"] = block["nextblockhash"]
        else:
            nxtTemplate = sqltemplateNoNext

        if "previousblockhash" in block:
            blockdict["previousblockhash"] = block["previousblockhash"]
        else:
            nxtTemplate = sqltemplateNoPrevious

        blockdict = setpools(block, blockdict)

        # Go get a bearer token from the JHipster UI, under Administration/API use "Try it out" for a block or a Tx and
        # grab the token from there. They are transient, so get a new one each session.
        blockdict["bearer"] = bearer
        nextblock = nxtTemplate.substitute(blockdict)

        #print "Next block: %s" % str(nextblock)
        dbblock(nextblock, cnxn, cursor)
        for tx in block["tx"]:
            txdict = {
                "tx": tx,
                "height": block["height"]
            }
            nexttx = sqltemplateTx.substitute(txdict)
            #print "Next Tx: " + nexttx
            #posttx(nexttx)
            dbtx(nexttx, cnxn, cursor)
        i = i + 1

if __name__ == "__main__":
    main()
