import React, { useState } from 'react';
import { Heir, RelationType } from '../types/models';

interface HeirFormProps {
    onAdd: (heir: Heir) => void;
    existingSpouse: boolean;
}

export const HeirForm: React.FC<HeirFormProps> = ({ onAdd, existingSpouse }) => {
    const [heir, setHeir] = useState<Heir>({
        name: '',
        relation: RelationType.CHILD,
        is_alive: true,
        children: []
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onAdd(heir);
        setHeir({
            name: '',
            relation: RelationType.CHILD,
            is_alive: true,
            children: []
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-white rounded-lg shadow">
            <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                    type="text"
                    value={heir.name}
                    onChange={(e) => setHeir({ ...heir, name: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Relationship</label>
                <select
                    value={heir.relation}
                    onChange={(e) => setHeir({ ...heir, relation: e.target.value as RelationType })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    required
                >
                    {!existingSpouse && <option value={RelationType.SPOUSE}>Spouse</option>}
                    <option value={RelationType.PARENT}>Parent</option>
                    <option value={RelationType.CHILD}>Child</option>
                    <option value={RelationType.GRANDPARENT}>Grandparent</option>
                </select>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Living Status</label>
                <div className="mt-1">
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            checked={heir.is_alive}
                            onChange={(e) => setHeir({ ...heir, is_alive: e.target.checked })}
                            className="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        />
                        <span className="ml-2">Is Alive</span>
                    </label>
                </div>
            </div>

            {heir.relation === RelationType.GRANDPARENT && (
                <div>
                    <label className="block text-sm font-medium text-gray-700">Side</label>
                    <select
                        value={heir.side || 'maternal'}
                        onChange={(e) => setHeir({ ...heir, side: e.target.value as 'maternal' | 'paternal' })}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        required
                    >
                        <option value="maternal">Maternal</option>
                        <option value="paternal">Paternal</option>
                    </select>
                </div>
            )}

            <button
                type="submit"
                className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
                Add Heir
            </button>
        </form>
    );
}; 