from django.shortcuts import render
from django.http import HttpResponse
from.coin_methods import *
from django.shortcuts import  render,redirect
from .models import *

"""
syntax for post for adding new peer - 
{"repl_name":"name","username","username"}


syntax for post for adding new transaction - 
{"transaction":{#transaction}}

syntax for post for making a new transaction - 
{"amount":#amount,"reciever_public_keyp1":#public key,"reciever_public_keyp2"}
"""
def read_blocked():
  blocked_peers=[]
  with open("blocked_urls.json", "r") as outfile:
      blocked_peers = json.load(outfile)
  return blocked_peers

def index(request):
  return render(request,'index.html')


def transaction_form(request):
  return render(request,"transaction_form.html")


def make_transaction(request):
  amount = request.POST['amount']
  if amount != None:
    reciever_public_keyp1 = request.POST['receiver_public_keyp1']
    reciever_public_keyp2 = request.POST['receiver_public_keyp2']
    transaction = eggchain.new_transaction(int(amount),[int(reciever_public_keyp1),int(reciever_public_keyp2)])
    if transaction:
      return redirect('index')
    else:
      return HttpResponse("your transaction is invalid, go back to the <a href='../'>home page</a>")
  return redirect('index')



def new_peer(request):
  for i in read_blocked():
    if i == "http://"+request.POST['repl_name']+"."+request.POST['username']+".repl.co":
      return HttpResponse("you are blocked")
  eggchain.write_new_peer("http://"+request.POST['repl_name']+"."+request.POST['username']+".repl.co")
  json_data = ""
  with open("peers.json","r") as outfile:
    json_data=outfile.read()
  return HttpResponse(json_data)


def new_transaction(request):
  transaction_recieved = eggchain.add_recieved_transaction(json.loads(request.POST["transaction"]))
  response = ""
  if transaction_recieved == True:
    response="true"
  else:
    response="false"
  return HttpResponse(response)


def new_block(request):
  block = eggchain.new_block_recieved(json.loads(request.POST['prevblock'])['nonce'],json.loads(request.POST['prevblock'])['transactions'],json.loads(request.POST['block'])['timestamp'],json.loads(request.POST['block'])['transactions'])
  if block == True:
    print("yes")
    eggchain.escape =True
    eggchain.log_all_blockchain_transactions(eggchain.chain[:-2])
    return HttpResponse("true")
  else:
    print("no")
    return HttpResponse("false")


def blockchain_response(request):
  chain = eggchain.chain
  return HttpResponse(json.dumps(chain))


def mine(request):
  if eggchain.mine_stat == False:
    eggchain.mine()
  return redirect('index')


def balance(request):
  eggchain.read_owned_coins()
  print(len(eggchain.coins))
  return render(request,'coin_count.html',{'count':len(eggchain.balance_everything(eggchain.chain)[0])})


def public_key(request):
  return HttpResponse("part 1 :<br>"+str(eggchain.jsonify_public_key(eggchain.public_key)[0])+"<br><br><br>"+"part 2 :<br>"+str(eggchain.jsonify_public_key(eggchain.public_key)[1]))
#copyright generationxcode & graphegg 2021


def get_block(request):
  try:
    number = int(request.POST['index'])
    block = Block_chain.objects.get(pk=number)
    return json.dumps({"index":block.id,"prev_hash":block.prev_hash,"nonce":int(block.nonce),"time_stamp":int(block.timestamp),"transactions":json.loads(block.transactions)})
  except:
    return HttpResponse("false")