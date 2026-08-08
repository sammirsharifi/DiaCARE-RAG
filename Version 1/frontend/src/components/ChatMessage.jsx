import Typewriter from "./Typewriter";


export default function ChatMessage({

    message,

    isLatest

}) {


    const isUser =
        message.role === "user";



    const evidenceText =

        message.evidence

        ?

        `


--------------------
Evidence
--------------------

${
    typeof message.evidence === "string"

    ?

    message.evidence

    :

    JSON.stringify(
        message.evidence,
        null,
        2
    )
}

`

        :

        "";



    const fullText =
        message.text + evidenceText;



    return (

        <div

            className={

                isUser

                ?

                "chat-message user-message"

                :

                "chat-message assistant-message"

            }

        >



            <div className="avatar">

                {
                    isUser
                    ?
                    "👤"
                    :
                    "🤖"
                }

            </div>



            <div className="bubble">


                {


                    isUser || !isLatest

                    ?


                    fullText


                    :


                    <Typewriter

                        text={fullText}

                        speed={20}

                    />


                }



            </div>



        </div>

    );

}