import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const Blogs: React.FC = () => {
    const [markdown, setMarkdown] = useState('');

    useEffect(() => {
        // Assuming you have your markdown files in the public folder
        fetch('/path-to-your-markdown-file.md')
            .then(response => response.text())
            .then(text => setMarkdown(text));
    }, []);

    return <ReactMarkdown>{markdown}</ReactMarkdown>;
};

export default Blogs;
