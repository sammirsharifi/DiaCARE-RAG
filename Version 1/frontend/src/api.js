const API_URL = "http://127.0.0.1:8000";


export async function askQuestion(question) {


    const response = await fetch(
        `${API_URL}/chat`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                question: question
            }),
        }
    );


    if (!response.ok) {

        throw new Error(
            "API request failed"
        );

    }


    return await response.json();

}