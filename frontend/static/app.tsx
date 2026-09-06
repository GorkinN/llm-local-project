import React, { useState } from 'react';
import './style.css';

interface AppProps {}
interface AppState {
    prompt: string;
    response: string;
}

const App: React.FC<AppProps> = () => {
    const [prompt, setPrompt] = useState<AppState['prompt']>('');
    const [response, setResponse] = useState<AppState['response']>('');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const res = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });
        const data = await res.json();
        setResponse(data.text);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                <h1 className="text-2xl font-bold mb-6 text-center">Aider RAG Interface</h1>
                <form className="space-y-4" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="prompt" className="block text-sm font-medium text-gray-700">Enter your prompt</label>
                        <input 
                            type="text" 
                            id="prompt" 
                            className="mt-1 block w-full p-2 border border-gray-300 rounded-md" 
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                    </div>
                    <button 
                        type="submit" 
                        className="w-full py-2 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75"
                    >
                        Generate
                    </button>
                </form>
                {response && (
                    <div className="mt-6">
                        <h2 className="text-xl font-bold mb-2">Response</h2>
                        <p className="text-gray-700">{response}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default App;
