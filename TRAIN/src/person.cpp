/*
 * person.cpp
 */

#include "person.h"
#include <iostream>

using namespace std;

person::person() {}

person::~person(){}

// Example name: zhang sanchuan, 19940231

void person::findStr(string& pat_str, string psw, string str, char c) {

	// unsigned int pos = psw.find(str);
	string::size_type pos = psw.find(str);
	int len = str.length();
	if (len < 2){
		return;
	}
	 // author forgot that only format > 1 char can be consider a format like in paper said 
	
	//Note that, to improve accuracy, we match using the longestprefix rule and also only consider PII-segments with len ≥ 2. For example, if john06071982 matches John Smith’s account name “john0607”, it will be parsed into A1B5 using the longestprefix rule, but not N3B2. In addition, we have only considered full MMDDdates in the definition of B1 ∼ B10, yet many users tend to use an abbr. of date when possible (e.g., “198267” instead of “19820607”). Thus, when matching a birthday-based segment in the training phase, if an abbreviation happens, the tag related to the corresponding full segment will be counted by one; In the password generation process, both full and abbreviated date segments will be produced. For instance, both “john06071982” and “john671982” will be produced if the structure N3B2 is used for guess generation
	
	
	string flag = "";
	for (int i = 0; i < len; i++)
		flag += c;
	if (pos != string::npos) {
		for (unsigned int i = pos; i < pos + len; i++) {
			if (pat_str[i] != 'P')
				return;
		}
		pat_str.replace(pos, len, flag);
	}
	
}


// DO NOT NAME 'L' 'D' 'P' 'S'

void person::processPhone(string& pat_str, string psw) {
	if (phone == "")
		return;	


	findStr(pat_str, psw, phone, 'C');
}

void person::processName(string& pat_str, string psw) {
	if (name == "")
		return;
	string py = name; //zhang san chuan
	string name_str[30]; // zhang/san/chuan
	int name_len = 0;
	int py_len = py.length(), st = 0;
	for (int i = 0; i < py_len; i++) {
		if (py[i] == ' ') {
			if (py[i - 1] != '?')
				name_str[name_len++] = py.substr(st, i - st);
			st = i + 1;
		}
	}


	// the more discover format the better, algo priority format swap longest 
	// so more format is better

	string tmp[6];
	if (name_len == 0)
		return;
	for (int i = 0; i < name_len; i++) {
		if (i>0) {

			tmp[5] += name_str[i][0];
		}

		tmp[0] += name_str[i][0];
		tmp[1] += name_str[i];
		if (i != 0)
			tmp[2] += name_str[i];
	}
	tmp[3] = name_str[0];

	tmp[3][0] -= 32;
	tmp[4] = tmp[0].substr(1, tmp[0].length() - 1); //sc

	findStr(pat_str, psw, tmp[1], 'N'); // zhangsanchuan
	findStr(pat_str, psw, tmp[2] + name_str[0], 'a'); // sanchuanzhang, `a` means the form's label, below the same
	findStr(pat_str, psw, tmp[0], 'b'); // zsc
	findStr(pat_str, psw, tmp[2], 'c'); // sanchuan
	findStr(pat_str, psw, name_str[0], 'd'); // zhang
	// findStr(pat_str, psw, tmp[3], 'e'); // Zhang

	findStr(pat_str, psw, tmp[4] + name_str[0], 'f'); // sczhang
	findStr(pat_str, psw, name_str[0] + tmp[4], 'g'); // zhangsc

	if (name_len >= 2)
	{
	findStr(pat_str, psw, name_str[1], 'V'); // san
	}
	if (name_len == 3)
	{
	findStr(pat_str, psw, name_str[2], 'W'); // chuan
	}
	if (name_len == 4)
	{
	findStr(pat_str, psw, name_str[2]+name_str[3], 'W'); // chuan
	}

	if (name_len >= 1)
	{
	findStr(pat_str, psw, tmp[5] + name_str[0][0], 'X'); // scz
	}
	}
	// fundamental char >= 2 char , can create a fundamental format 

	// string tmp[10];
	// for (int i = 0; i < name_len; i++) {
	// 	tmp[0] += name_str[i][0];
	// 	tmp[1] = name_str[i]
	// 	if (i != 0)
	// 		tmp[2] += name_str[i];
	// }


void person::processBirth(string& pat_str, string psw) {
	if (birth == "" || birth.length() != 8)
		return;
	// findStr(pat_str, psw, birth, 'B'); // 19940231
	// if (birth[4] == '0')
	// 	findStr(pat_str, psw, birth.substr(0, 4) + birth.substr(5, 3), 'h'); // 1994231
	// if (birth[6] == '0')
	// 	findStr(pat_str, psw, birth.substr(0, 6) + birth[7], 'i'); // 1994021
	// if (birth[4] == '0' && birth[6] == '0')
	// 	findStr(pat_str, psw, birth.substr(0, 4) + birth[5] + birth[7], 'j'); // 199421
	// findStr(pat_str, psw, birth.substr(0, 6), 'k'); // 199402
	// findStr(pat_str, psw, birth.substr(2, 6), 'l'); // 940231
	// findStr(pat_str, psw,t birth.substr(0, 4), 'm'); // 1994
	// findStr(pat_str, psw, birth.substr(4, 4), 'n'); // 0231
	// findStr(pat_str, psw, birth.substr(2, 4), 'o'); // 9402

	// findStr(pat_str, psw, birth.substr(4, 4) + birth.substr(0, 4), 'p'); // 02311994
	// findStr(pat_str, psw, birth.substr(4, 2) + birth.substr(0, 4), 'q'); // 021994
	// findStr(pat_str, psw, birth.substr(4, 4) + birth.substr(2, 2), 'r'); // 023194
	
	// collecting fundamentals : 7 of them 
	// date , month , year, date transform, month trans , year trans
	findStr(pat_str, psw, birth.substr(4,2) , 'O'); // month
	findStr(pat_str, psw, birth.substr(6,2) , 'Q'); // date
	findStr(pat_str, psw, birth.substr(0,4) , 'R'); // year
	findStr(pat_str, psw, birth.substr(2,2) , 'F'); // last 2 digit year
	// just need to > 1 char to be count as format 
	// for now, most pass is date-month-year order
	if (birth[4] == '0'&& birth[6] != '0')
	// month with 0 as first digit  + full year / partial year / full date
		findStr(pat_str, psw, birth.substr(5, 1) + birth.substr(0,4), 'H'); 
		findStr(pat_str, psw, birth.substr(5, 1) + birth.substr(2,2), 'I'); 
		findStr(pat_str, psw, birth.substr(5, 1) + birth.substr(6,2), 'J'); 
	if (birth[6] == '0'&& birth[4] != '0')
	 // date with 0 as first digit+ full year / partial year / full month
		findStr(pat_str, psw, birth.substr(7,1) + birth.substr(0,4), 'K');
		findStr(pat_str, psw, birth.substr(7,1) + birth.substr(2,2), 'Y');
		findStr(pat_str, psw, birth.substr(7,1) + birth.substr(4,2), 'Z');
	if (birth[6] == '0' && birth[4] == '0')
		findStr(pat_str, psw, birth.substr(7,1) + birth.substr(5, 1), 'M');


}

void person::processEmail(string& pat_str, string psw) {
	int pos = email.find('@');
	if (email == "" || pos == string::npos)
		return;
	findStr(pat_str, psw, email.substr(0, pos), 'E'); // email preix
	string email_d = "", email_l = "", email_pre = email.substr(0, pos);
	bool dd = 0, ll = 0;
	for (int i = 0; i < pos; i++) {
		if (email_pre[i] >= '0' && email_pre[i] <= '9') {
			email_d += email_pre[i];
			dd = 1;
		} else {
			if (dd == 1)
				break;
		}
	}

	if (dd == 1 && email_d != email_pre)
		findStr(pat_str, psw, email_d, 's'); // email prefix first D string

	for (int i = 0; i < pos; i++) {
		if (email_pre[i] >= 'a' && email_pre[i] <= 'z' || email_pre[i] >= 'A'
				&& email_pre[i] <= 'Z') {
			email_l += email_pre[i];
			ll = 1;
		} else {
			if (ll == 1)
				break;
		}
	}
	if (ll == 1 && email_l != email_pre)
		findStr(pat_str, psw, email_l, 't'); // email prefix first L string 
}
void person::processAccount(string& pat_str, string psw) {
	if (account == "")
		return;
	findStr(pat_str, psw, account, 'A');
	string acc_d = "", acc_l = "", acc = account;
	int acclen = account.length();
	bool ad = 0, al = 0;
	for (int i = 0; i < acclen; i++) {
		if (acc[i] >= '0' && acc[i] <= '9') {
			acc_d += acc[i];
			ad = 1;
		} else {
			if (ad == 1)
				break;
		}
	}
	if (ad == 1 && acc_d != acc)
		findStr(pat_str, psw, acc_d, 'u'); // username prefix first D string 

	for (int i = 0; i < acclen; i++) {
		if (acc[i] >= 'a' && acc[i] <= 'z' || acc[i] >= 'A' && acc[i] <= 'Z') {
			acc_l += acc[i];
			al = 1;
		} else {
			if (al == 1)
				break;
		}
	}
	if (al == 1 && acc_l != acc)
		findStr(pat_str, psw, acc_l, 'v'); // username prefix first L string 
}
void person::processGid(string& pat_str, string psw) {
	if (gid == "" && gid.length()!=18)
		return;
	int len = gid.length();
	findStr(pat_str, psw, gid, 'G');
	findStr(pat_str, psw, gid.substr(len - 4, 4), 'w');
}