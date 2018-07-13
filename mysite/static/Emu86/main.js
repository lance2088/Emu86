/**
 * Created by Varun on 19/06/17.
 */

function AlertError()
{
    var raised=document.getElementById("error")

    if(raised)
    {
        raised=raised.value;
        if (raised != "") 
        {
            alert(document.getElementById("error").value);
        }
    }
}

function loadcode()
{
    if(sessionStorage.loadonce)
    {
        AlertError();
        var instr = document.getElementsByName("last_instr")[0];
        var mips_ip = document.getElementsByName("PC");
        var intel_ip = document.getElementsByName("EIP");
        var ip_val = null;
        if (mips_ip.length != 0){
            ip_val = parseInt(mips_ip[0].value)/4;
        }
        else if (intel_ip.length != 0) {
            ip_val = parseInt(intel_ip[0].value);
        }
        if (instr && ip_val) {
            var input = document.getElementById("id_code");
            var countCode = 0;
            var countRepeats = 0;
            var codeArray = input.value.split("\n");
            var textArea = true; 
            if (instr.value != "") {
                for (var index = 0; index < codeArray.length; index++) {
                    var string = codeArray[index].trim();
                    if (countCode == ip_val){
                        break;
                    }
                    if (string == ".data"){
                        textArea = false;
                        continue;
                    }
                    else if (string == ".text"){
                        textArea = true;
                        continue;
                    }
                    if (!(string === "") && textArea && string[0] != ";"){
                        countCode++; 
                    }
                    if (string == instr.value){
                        countRepeats++;
                    }
                }
                input.focus();
                var startIndex = 0;
                for (var time = 0; time < countRepeats; time++) {
                    startIndex = input.value.indexOf(instr.value, startIndex) 
                                 + instr.value.length;
                }
                startIndex -= instr.value.length;
                input.setSelectionRange(startIndex, 
                       startIndex + instr.value.length);
            }
        }
        return;
    }
    else
    {
        sessionStorage.loadonce=1;
        code = localStorage.Code;
        if(code!=undefined || code!=null) {
            document.getElementById("id_code").value = code;
        }
    }
}


function Savecode()
{
    if(confirm("Do you want to save this code?")) {
        data = document.getElementById("id_code").value;
        try {
            localStorage.Code=data;
            alert("Your code was saved successfully.");
        }
        catch(exception)
        {
            alert("An unknown error occured, please try again.");

        }
    }
}

function convert(name,value)
{
    var message= "Binary value of " + " " + name + ": ";
    var value1=parseInt(value)
    if(value1>=0) {

        message=message+((value1).toString(2));
        alert(message);
    }
    else
    {
        message=message+((value1>>>0).toString(2));
        alert(message);
    }
}