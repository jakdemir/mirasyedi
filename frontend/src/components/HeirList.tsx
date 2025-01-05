import React from 'react';
import { Heir, RelationType, FamilyTree } from '../types';
import { TrashIcon } from '@heroicons/react/24/outline';

interface HeirListProps {
    familyTree: FamilyTree;
    onRemove: (name: string) => void;
}

export const HeirList: React.FC<HeirListProps> = ({ familyTree, onRemove }) => {
    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    };

    const getGroupBackgroundColor = (relation: RelationType) => {
        switch (relation) {
            case RelationType.SPOUSE:
                return 'bg-indigo-50';
            case RelationType.CHILD:
                return 'bg-emerald-50';
            case RelationType.PARENT:
                return 'bg-amber-50';
            case RelationType.GRANDPARENT:
                return 'bg-rose-50';
            default:
                return '';
        }
    };

    const getGroupTextColor = (relation: RelationType) => {
        switch (relation) {
            case RelationType.SPOUSE:
                return 'text-indigo-800';
            case RelationType.CHILD:
                return 'text-emerald-800';
            case RelationType.PARENT:
                return 'text-amber-800';
            case RelationType.GRANDPARENT:
                return 'text-rose-800';
            default:
                return '';
        }
    };

    const renderHeirRow = (heir: Heir, index: number, depth = 0, parentRelation?: RelationType) => {
        const baseColor = parentRelation ? getGroupBackgroundColor(parentRelation) : getGroupBackgroundColor(heir.relation);
        const textColor = parentRelation ? getGroupTextColor(parentRelation) : getGroupTextColor(heir.relation);
        const rowColor = depth > 0 ? `${baseColor} bg-opacity-${60 - depth * 10}` : baseColor;
        
        return (
            <React.Fragment key={`${heir.name}-${heir.relation}-${index}`}>
                <tr className={`${rowColor} hover:bg-opacity-80 transition-colors duration-150`}>
                    <td className={`py-4 pr-3 text-sm font-medium ${textColor}`} style={{ paddingLeft: `${depth * 2 + 1}rem` }}>
                        {depth > 0 ? '└─ ' : ''}{heir.name}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-600">
                        {heir.relation}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-600">
                        {heir.is_alive ? 'Alive' : 'Deceased'}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-600">
                        {heir.branch || '-'}
                    </td>
                    <td className={`whitespace-nowrap px-3 py-4 text-sm font-medium ${heir.share ? textColor : 'text-gray-500'}`}>
                        {heir.share ? formatCurrency(heir.share) : '-'}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-600">
                        {heir.children && heir.children.length > 0 && heir.is_alive ? heir.children.length : '-'}
                    </td>
                    <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium">
                        <button
                            onClick={() => onRemove(heir.name)}
                            className="text-red-600 hover:text-red-900 transition-colors duration-150"
                        >
                            <TrashIcon className="h-5 w-5" aria-hidden="true" />
                        </button>
                    </td>
                </tr>
                {!heir.is_alive && heir.children && heir.children.length > 0 && (
                    heir.children.map((child, childIndex) => 
                        renderHeirRow(child, childIndex, depth + 1, heir.relation)
                    )
                )}
            </React.Fragment>
        );
    };

    const renderFamilyGroup = (heirs: Heir[]) => {
        return heirs.map((heir, index) => renderHeirRow(heir, index));
    };

    const renderGroupHeader = (title: string, relation: RelationType) => {
        const bgColor = getGroupBackgroundColor(relation);
        const textColor = getGroupTextColor(relation);
        return (
            <tr className={`${bgColor} bg-opacity-80 border-t border-b`}>
                <td colSpan={7} className={`py-2 pl-4 pr-3 text-sm font-bold ${textColor}`}>
                    {title}
                </td>
            </tr>
        );
    };

    return (
        <div className="bg-white rounded-lg shadow overflow-hidden">
            <h3 className="text-lg font-medium leading-6 text-gray-900 p-4 border-b">Family Tree</h3>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-300">
                    <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Name</th>
                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Relation</th>
                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Living Status</th>
                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Branch</th>
                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Share</th>
                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Children</th>
                            <th scope="col" className="relative py-3.5 pl-3 pr-4">
                                <span className="sr-only">Actions</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {familyTree.spouse && (
                            <>
                                {renderGroupHeader('Spouse', RelationType.SPOUSE)}
                                {renderHeirRow(familyTree.spouse, 0)}
                            </>
                        )}
                        
                        {familyTree.children && familyTree.children.length > 0 && (
                            <>
                                {renderGroupHeader('Children', RelationType.CHILD)}
                                {renderFamilyGroup(familyTree.children)}
                            </>
                        )}
                        
                        {(familyTree.mother || familyTree.father) && (
                            <>
                                {renderGroupHeader('Parents', RelationType.PARENT)}
                                {familyTree.mother && renderHeirRow(familyTree.mother, 0)}
                                {familyTree.father && renderHeirRow(familyTree.father, 0)}
                            </>
                        )}
                        
                        {familyTree.maternal_grandparents && familyTree.maternal_grandparents.length > 0 && (
                            <>
                                {renderGroupHeader('Maternal Grandparents', RelationType.GRANDPARENT)}
                                {renderFamilyGroup(familyTree.maternal_grandparents)}
                            </>
                        )}
                        
                        {familyTree.paternal_grandparents && familyTree.paternal_grandparents.length > 0 && (
                            <>
                                {renderGroupHeader('Paternal Grandparents', RelationType.GRANDPARENT)}
                                {renderFamilyGroup(familyTree.paternal_grandparents)}
                            </>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}; 