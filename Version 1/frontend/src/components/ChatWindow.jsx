import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";


export default function ChatWindow({

    messages,

    loading

}) {


    return (

        <div className="chat-window">


            {
                messages.map(
                    (message, index) => (

                        <ChatMessage

                            key={index}

                            message={message}

                            isLatest={
                                index === messages.length - 1
                            }

                        />

                    )
                )
            }



            {
                loading && (

                    <div className="chat-message assistant-message">


                        <div className="avatar">
                            🤖
                        </div>


                        <div className="bubble">

                            <TypingIndicator />

                        </div>


                    </div>

                )
            }



        </div>

    );

}