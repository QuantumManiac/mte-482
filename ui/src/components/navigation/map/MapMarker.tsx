import React, { useEffect, useRef, useState } from 'react';
import { type Coordinate } from '~/types/Navigation';

interface MapMarkerProps {
    pos: Coordinate;
    icon: string;
    tooltipText?: string | null;
}

export default function MapMarker({pos, icon, tooltipText}: MapMarkerProps) {
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
    left: `${pos.x}px`,
    top: `${pos.y}px`,
    transform: `translate(-50%, -50%)`, // Applying rotation
  };

  return (
    <div
      className="absolute flex items-center justify-center"
      style={style} // Applying dynamic styles for rotation and positioning
      ref={pointRef}
    >
      <span
        className="text-2xl" // Using Tailwind's text size scale
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
