import { useEffect, useState } from "react";

import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";

import { askQuestion } from "./api";

import "./styles/chat.css";


export default function App() {


    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);



    useEffect(() => {


        setMessages([

            {
                role: "assistant",

                text:
               `Hello 👋

I am an AI assistant for diabetes-related questions. This system uses Explainable GraphRAG to provide answers supported by knowledge graph evidence.

Project:
https://github.com/sammirsharifi/DiaCARE-RAG

Ask your question.`
            }

        ]);


    }, []);





    async function handleSend(question){


        if(!question.trim())
            return;



        const userMessage = {

            role:"user",

            text:question

        };



        setMessages(
            previous => [
                ...previous,
                userMessage
            ]
        );



        setLoading(true);



        try{


            const result =
                await askQuestion(question);



            const assistantMessage = {


                role:"assistant",


                text:
                    result.answer
                    ||
                    "No answer received.",


                evidence:
                    result.evidence

            };



            setMessages(
                previous => [
                    ...previous,
                    assistantMessage
                ]
            );



        }


        catch(error){


            setMessages(
                previous => [

                    ...previous,

                    {

                        role:"assistant",

                        text:
                        "Backend Error. Unable to generate response."

                    }

                ]
            );


        }


        finally{


            setLoading(false);


        }


    }





    return (

        <div className="app">


            <div className="chat-container">


                <ChatWindow

                    messages={messages}

                    loading={loading}

                />



                <InputBox

                    onSend={handleSend}

                />


            </div>


        </div>

    );


}