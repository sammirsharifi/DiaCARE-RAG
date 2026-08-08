import EvidencePanel from "./EvidencePanel";


function Message({
    message
}){


return (

<div
className={
message.role === "user"
?
"user-message"
:
"assistant-message"
}
>


<p>
{message.content}
</p>



{
message.evidence &&

<EvidencePanel

data={message.evidence}

/>

}


</div>


)

}


export default Message;