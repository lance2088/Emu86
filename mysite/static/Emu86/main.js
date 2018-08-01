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

function selectSample()
{
    selectBar = document.getElementsByName("sample")[0];
    var selected = selectBar.options[selectBar.selectedIndex].value
    var flav = document.getElementsByName("flavor")[0];
    if (flav){
        if (selected == "none"){
            document.getElementById("id_code").value = "";
        }
        else if (selected == "addTwo") {
            addTwo(flav.value);
        }
        else if (selected == "arithExpr") {
            arithExpr(flav.value);
        }
        else if (selected == "log") {
            log(flav.value);
        }
        else if (selected == "modify") {
            modify(flav.value);
        }
        else if (selected == "loop") {
            loop(flav.value);
        }
        else if (selected == "avg") {
            avg(flav.value);
        }
        else if (selected == "celFah") {
            celFah(flav.value);
        }
        else if (selected == "sqrt") {
            sqrt(flav.value);
        }
        else if (selected == "area") {
            area(flav.value);
        }
        else if (selected == "power") {
            power(flav.value);
        }
        else if (selected == "arithShift") {
            arithShift(flav.value);
        }
        else if (selected == "data") {
            data(flav.value);
        }
        else if (selected == "keyInterrupt") {
            keyInterrupt(flav.value);
        }
        else if (selected == "array") {
            array(flav.value);
        }
    }
}

function checkForScript()
{
    data = document.getElementById("id_code").value;
    if (data.indexOf("<script>") != -1){
        var temp_val = data.split("<script>");
        data = temp_val.join("");
    }
    if (data.indexOf("</script>") != -1){
        var temp_val = data.split("</script>");
        data = temp_val.join("");
    }
    document.getElementById("id_code").value = data;
}

function loadcode()
{
    if(sessionStorage.loadonce)
    {
        AlertError();
        var instr = document.getElementsByName("last_instr")[0];
        var lastInstr = instr.value;
        if (lastInstr.indexOf(": Exiting program") != -1){
            lastInstr = lastInstr.substring(0, lastInstr.indexOf(": Exiting program"));
        }
        var mips_ip = document.getElementsByName("PC");
        var intel_ip = document.getElementsByName("EIP");
        var ip_val = null;
        var hex_or_dec = null;
        var radios = document.getElementsByName("base");
        for (var index = 0; index < radios.length; index++) {
            if (radios[index].checked) {
                hex_or_dec = radios[index].value;
                break;
            }
        }
        if (mips_ip.length != 0){
            if (hex_or_dec == "hex") {
                ip_val = parseInt(mips_ip[0].value, 16)/4;
            }
            else {
                ip_val = parseInt(mips_ip[0].value)/4;
            }
        }
        else if (intel_ip.length != 0) {
            if (hex_or_dec == "hex") {
                ip_val = parseInt(intel_ip[0].value, 16);
            }
            else {
                ip_val = parseInt(intel_ip[0].value);
            }
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
                    if (string == lastInstr){
                        countRepeats++;
                    }
                }
                input.focus();
                var startIndex = 0;
                for (var time = 0; time < countRepeats; time++) {
                    startIndex = input.value.indexOf(lastInstr, startIndex) 
                                 + lastInstr.length;
                }
                startIndex -= lastInstr.length;
                input.setSelectionRange(startIndex, 
                       startIndex + lastInstr.length);
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
    var flav = document.getElementsByName("flavor")[0].value;
    var file_name = null;
    if (flav == "mips"){
        file_name = prompt("Please enter file name to save as, ending in .asm or .txt (for binary code): ");
    }
    else{
        file_name = prompt("Please enter file name to save as, ending in .asm: ");
    }
    if (file_name == null){
        alert("Save cancelled");
    }
    else if (file_name == ""){
        alert("Invalid file name");
    }
    else if (file_name.length < 5){
        alert("Invalid file name: " + file_name);
    }
    else if (flav == "mips" && file_name.slice(file_name.length - 4) != ".asm" && file_name.slice(file_name.length - 4) != ".txt" ) {
        alert("Invalid file name: " + file_name);
    }
    else if (flav != "mips" && file_name.slice(file_name.length - 4) != ".asm"){
        alert("Invalid file name: " + file_name);
    }
    else {
        data = null;
        if (file_name.slice(file_name.length - 4) == ".asm"){
            data = document.getElementById("id_code").value;
        }
        else{
            data = document.getElementsByName("bit_code")[0].value;
        }
        var file_blob = new Blob([data], {type: 'text/plain'});
        if (window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveOrOpenBlob(file_blob, file);
        }
        else {
            var anchor = document.createElement('a'),
            url = URL.createObjectURL(file_blob);
            anchor.href = url;
            anchor.download = file_name;
            document.body.appendChild(anchor);
            anchor.click();
            document.body.removeChild(anchor);
            window.URL.revokeObjectURL(url);  
        }
    }
}

function SubmitForm(){
    document.getElementById("codeForm").submit();
    document.getElementById("clear-button").disabled="true";
    document.getElementById("run-button").disabled="true";
    document.getElementById("save-button").disabled="true";
    document.getElementById("step-button").disabled="true";
}

function clearButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("clear-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "clear";
            SubmitForm();
        }
    }
}

function runButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("run-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "run";
            SubmitForm();
        }
    }
}

function stepButton(){
    if (document.readyState == "complete") {
        if (document.getElementById("step-button").hasAttribute("disabled") == false){
            document.getElementsByName("button_type")[0].value = "step";
            SubmitForm();
        }
    }
}

function convert(name,value)
{
    var message= "Binary value of " + " " + name + ": ";
    var hex_or_dec = null;
    var radios = document.getElementsByName("base");
    for (var index = 0; index < radios.length; index++) {
        if (radios[index].checked) {
            hex_or_dec = radios[index].value;
            break;
        }
    }
    var value1 = null;
    if (hex_or_dec == "hex"){
        value1=parseInt(value, 16);
    }
    else{
        value1=parseInt(value);
    }
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

// function AddMem()
// {
//     var loc = document.getElementById("memText").value;
//     var val = document.getElementById("valueText").value;
//     var repeat = document.getElementById("repeatText").value;
//     if (loc == ""){
//         alert("Cannot set an invisible location");
//     }
//     else if (val == ""){
//         alert("Cannot set using an invisible value");
//     }
//     if (repeat != ""){
//         repeat = parseInt(repeat);
//     }
//     else {
//         repeat = 0;
//     }
//     for (var i = 0; i <= repeat; i++) {
        
//     }
// }