import {useEffect, useState} from "react";

interface FileItem {
    id: number;
    name: string;
    path: string;
    type: string;
    status: string;
    created_at: string;
    updated_at: string;
}

export default function SourceFilesApp() {
    const [files, setFiles] = useState<FileItem[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/v1/files/")
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => setFiles(data.data.files))
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <p>Loading files...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="p-4 flex justify-center">
            <div className="w-4/5">
                <h2 className="text-xl font-bold mb-4 text-center">Available Files</h2>
                <table className="w-full border-4 border-gray-600 border-collapse">
                    <thead>
                    <tr className="bg-gray-300 border border-gray-600">
                        <th className="border border-gray-400 p-2">ID</th>
                        <th className="border border-gray-400 p-2">Name</th>
                        <th className="border border-gray-400 p-2">Path</th>
                        <th className="border border-gray-400 p-2">Type</th>
                        <th className="border border-gray-400 p-2">Status</th>
                        <th className="border border-gray-400 p-2">Created At</th>
                    </tr>
                    </thead>
                    <tbody>
                    {files.length === 0 ? (
                        <tr>
                            <td colSpan={6} className="border border-gray-400 p-2 text-center">No files available</td>
                        </tr>
                    ) : (
                        files.map((file) => (
                            <tr key={file.id} className="border border-gray-400">
                                <td className="border border-gray-400 p-2">{file.id}</td>
                                <td className="border border-gray-400 p-2">{file.name}</td>
                                <td className="border border-gray-400 p-2">{file.path}</td>
                                <td className="border border-gray-400 p-2">{file.type}</td>
                                <td className="border border-gray-400 p-2">{file.status}</td>
                                <td className="border border-gray-400 p-2">{new Date(file.created_at).toLocaleString()}</td>
                            </tr>
                        ))
                    )}
                    </tbody>
                </table>
                <p className="mt-4 text-right font-bold">Total Files: {files.length}</p>
            </div>
        </div>
    );
}