import React, { useEffect, useRef, useState } from 'react';

interface MapMarkerProps {
    x: number;
    y: number;
    icon: string;
    tooltipText?: string | null;
}

export default function MapMarker({x, y, icon, tooltipText}: MapMarkerProps) {
  const [isTooltipVisible, setIsTooltipVisible] = useState(false);
  const pointRef = useRef<HTMLDivElement>(null);

  const toggleTooltip = () => {
    setIsTooltipVisible(!isTooltipVisible);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (pointRef.current && !pointRef.current.contains(event.target as Node)) {
      setIsTooltipVisible(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const style = {
    left: `${x}px`,
    top: `${y}px`,
  };

  return (
    <div
      className="absolute flex items-center justify-center"
      style={style} // Applying dynamic styles for rotation and positioning
      ref={pointRef}
    >
      <span
        className="text-3xl" // Using Tailwind's text size scale
        onClick={toggleTooltip}
      >
        {icon}
      </span>
      {isTooltipVisible && (
        <div
          className="absolute -translate-x-1/2 bg-white text-l p-2 border-2 rounded-md border-black"
          style={{ bottom: '100%' }}
        >
          {tooltipText}
        </div>
      )}
    </div>
  );
}
