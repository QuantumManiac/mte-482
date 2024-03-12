'use client'

import { useRef, useEffect, useState } from 'react';

interface DynamicFontSizeTextProps {
    text: string;
}

export default function DynamicFontSizeText({text}: DynamicFontSizeTextProps) {
    const textRef = useRef<HTMLParagraphElement>(null);
    const [fontSize, setFontSize] = useState<number>(16); // Starting font size

    useEffect(() => {
        const adjustFontSize = (): void => {
        if (!textRef.current) return;

        const parent = textRef.current.parentNode as HTMLElement;
        let currentSize = fontSize;

        // Reset font size to measure initial overflow
        textRef.current.style.fontSize = `${currentSize}px`;

        // Increase font size until it overflows
        while (parent.scrollHeight === parent.clientHeight && currentSize < 100) { // 100 is a max font size limit
            currentSize++;
            textRef.current.style.fontSize = `${currentSize}px`;
        }

        // Decrease font size by one to ensure no overflow
        textRef.current.style.fontSize = `${currentSize - 1}px`;
        setFontSize(currentSize - 1);
        };

        adjustFontSize();
    }, [text, fontSize]); // Re-run effect if the text changes or fontSize changes

    return (
        <p ref={textRef} style={{ fontSize: `${fontSize}px` }}>
        {text}
        </p>
    );
}
