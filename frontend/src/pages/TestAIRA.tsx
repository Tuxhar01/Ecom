import { useState } from 'react';
import { testAPI } from '../services/api';

export default function TestAIRA() {
  const [results, setResults] = useState<{ [key: string]: any }>({});
  const [loading, setLoading] = useState<{ [key: string]: boolean }>({});

  const runTest = async (testName: string, testFn: () => Promise<any>) => {
    setLoading(prev => ({ ...prev, [testName]: true }));
    try {
      const result = await testFn();
      setResults(prev => ({ ...prev, [testName]: { success: true, data: result } }));
    } catch (error: any) {
      setResults(prev => ({ 
        ...prev, 
        [testName]: { 
          success: false, 
          error: error.response?.data || error.message 
        } 
      }));
    } finally {
      setLoading(prev => ({ ...prev, [testName]: false }));
    }
  };

  const tests = [
    {
      name: 'Database Error (P0)',
      key: 'database',
      fn: testAPI.triggerDatabaseError,
      description: 'Simulates a critical database connection failure'
    },
    {
      name: 'Authentication Error (P1)',
      key: 'auth',
      fn: testAPI.triggerAuthError,
      description: 'Simulates an authentication/security error'
    },
    {
      name: 'Payment Error (P1)',
      key: 'payment',
      fn: testAPI.triggerPaymentError,
      description: 'Simulates a payment processing failure'
    },
    {
      name: 'Validation Error (P2)',
      key: 'validation',
      fn: testAPI.triggerValidationError,
      description: 'Simulates input validation errors'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🧪 AIRA Error Testing
          </h1>
          <p className="text-gray-600 mb-4">
            Test AIRA log monitoring by triggering different error types. 
            Check your AIRA dashboard to see incidents being created.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Note:</strong> These endpoints intentionally throw errors to test AIRA integration.
              Each error will be logged and sent to your AIRA dashboard with appropriate severity levels.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {tests.map(test => (
            <div key={test.key} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {test.name}
                  </h3>
                  <p className="text-sm text-gray-600">{test.description}</p>
                </div>
                <button
                  onClick={() => runTest(test.key, test.fn)}
                  disabled={loading[test.key]}
                  className={`ml-4 px-4 py-2 rounded-lg font-medium transition-colors ${
                    loading[test.key]
                      ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      : 'bg-red-600 text-white hover:bg-red-700'
                  }`}
                >
                  {loading[test.key] ? 'Testing...' : 'Trigger Error'}
                </button>
              </div>

              {results[test.key] && (
                <div className={`mt-4 p-4 rounded-lg ${
                  results[test.key].success 
                    ? 'bg-yellow-50 border border-yellow-200' 
                    : 'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex items-start">
                    <span className="text-2xl mr-3">
                      {results[test.key].success ? '⚠️' : '❌'}
                    </span>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 mb-2">
                        {results[test.key].success ? 'Error Triggered Successfully' : 'Request Failed'}
                      </p>
                      <pre className="text-sm bg-white p-3 rounded border overflow-x-auto">
                        {JSON.stringify(
                          results[test.key].success 
                            ? results[test.key].data 
                            : results[test.key].error, 
                          null, 
                          2
                        )}
                      </pre>
                      {results[test.key].success && (
                        <p className="mt-2 text-sm text-gray-600">
                          ✅ Check your AIRA dashboard - this error should appear as a new incident!
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            📊 How to Verify
          </h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>Click any "Trigger Error" button above</li>
            <li>Wait for the error response (should be immediate)</li>
            <li>Open your AIRA dashboard</li>
            <li>Look for a new incident with the corresponding error message</li>
            <li>Verify the incident includes:
              <ul className="list-disc list-inside ml-6 mt-1 text-sm">
                <li>Correct severity level (P0/P1/P2)</li>
                <li>Stack trace</li>
                <li>Request context (URL, method, headers)</li>
                <li>Timestamp</li>
              </ul>
            </li>
          </ol>
        </div>

        <div className="mt-6 bg-gray-100 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            🔍 Backend Logs
          </h3>
          <p className="text-sm text-gray-600 mb-2">
            Check your Render logs for these messages after triggering errors:
          </p>
          <pre className="text-xs bg-gray-800 text-green-400 p-4 rounded overflow-x-auto">
{`[AIRA] emit() called - enabled: True, level: ERROR
[AIRA] Processing error: [Error message]
[AIRA] Payload built, sending to https://aira-1-yxlx.onrender.com/webhook
[AIRA] Attempting to send to webhook...
[AIRA] Attempt 1/3
[AIRA] Response status: 200
[AIRA] Successfully sent error to AIRA`}
          </pre>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
