import React from 'react';
import { GearIcon } from './icons/GearIcon';

const ConversionApi = () => (
  <div className="text-center py-16">
    <GearIcon />
    <h2 className="text-3xl font-bold text-dark-charcoal mt-4">Conversion API</h2>
    <p className="text-gray-600 mt-2">With passion to Developers</p>
    <div className="mt-6 space-x-4">
      <a href="#" className="border border-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-100">Documentation</a>
      <a href="#" className="border border-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-100">PHP Example</a>
      <a href="#" className="border border-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-100">Get an API Key</a>
    </div>
  </div>
);

export default ConversionApi;