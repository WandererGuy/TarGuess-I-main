the csv needs little correction before been put through general preprocess API, so that preprocess have easier time <br>
because tailieuvn breach and zingvn breach is very different , <br>
so a general fix approach is not possible , requires very complicated heuristic approach, so <br>
i tailor different preprocess for each of them before put through a general preprocess API , which fix name , replace plain cracked password<br>
- fix column name 
- make sure there is firstname , lastname column 
- remove line which have excessive or missing column 


the example output of those script is in process_output_sample

a csv or xlsx file have 
id,username,password,email,firstname,lastname,birthday,tel

'id', 'username', 'password', 'email', 'firstname', 'lastname', 'birthday', 'tel'
where:
id : from 1 and increasing
first name : Ten chinh (main name in vitenamese)
last name : Ho va ten dem (familu name + surname in vietnamese)
birthday : ex. 19-1-1985
username : username he/she use on one website 
password : in MD5 form
email : ex. manh30k@gmail.com
tel: telephone 