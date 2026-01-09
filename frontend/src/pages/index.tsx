import { useState } from 'react';
import Head from 'next/head';
import ChatInterface from '@/components/ChatInterface';
import DocumentManager from '@/components/DocumentManager';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'documents'>('chat');

  return (
    <>
      <Head>
        <title>LangChain App Boilerplate</title>
        <meta name="description" content="Production-grade LangChain application" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gray-100">
        <div className="container mx-auto py-8">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="border-b">
              <nav className="flex">
                <button
                  onClick={() => setActiveTab('chat')}
                  className={`px-6 py-4 font-medium ${
                    activeTab === 'chat'
                      ? 'border-b-2 border-blue-500 text-blue-600'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Chat
                </button>
                <button
                  onClick={() => setActiveTab('documents')}
                  className={`px-6 py-4 font-medium ${
                    activeTab === 'documents'
                      ? 'border-b-2 border-blue-500 text-blue-600'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Documents
                </button>
              </nav>
            </div>

            <div className="p-6" style={{ minHeight: '600px' }}>
              {activeTab === 'chat' ? <ChatInterface /> : <DocumentManager />}
            </div>
          </div>

          <div className="mt-4 text-center text-gray-600 text-sm">
            <p>LangChain App Boilerplate - Production-grade starter template</p>
          </div>
        </div>
      </main>
    </>
  );
}
