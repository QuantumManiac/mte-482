'use client'

import { useState } from "react";

import ActionButton from "./ActionButton";
import DynamicFontSizeText from "./DynamicFontSizeText";

interface ExpandedViewButtonProps {
    text: string;
}

export default function ExpandedViewText({text}: ExpandedViewButtonProps) {
  const [expanded, setExpanded] = useState<boolean>(false);

  return (
    <>
      <div className="flex flex-row absolute right-0 bottom-0">
        <ActionButton style={"bg-blue-400"} text="Expand" icon="🔍" onClick={() => {setExpanded(true)}}/>
      </div>
      {expanded && (
        <div className="fixed z-50 top-0 left-0 w-screen h-screen bg-white p-4 flex" onClick={() => setExpanded(false)}>
          <DynamicFontSizeText text={text} />
          <ActionButton style={"fixed right-0 bottom-0 bg-red-500"} text="Close" icon="✖️" onClick={() => {setExpanded(true)}}/>
        </div>
      )}
    </>
  );
}
