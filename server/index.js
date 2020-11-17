const express = require('express')
const cors = require('cors')
const app = express()
app.use(cors())
app.use(express.static(__dirname+'/public'))
let data = ''

app.get('/',(req,res)=>{
	res.sendfile("index.html")
})

app.get('/refresh',(req,res)=>{
	res.send(data)
})
app.get('/update',(req,res)=>{
	console.log(req.query)
	data = req.query
	res.send('OK')
})
 
app.listen(1234,()=>{
	console.log("Connected to port 1234..")
})
