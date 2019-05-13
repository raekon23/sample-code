import React from 'react';
import { shallow } from 'enzyme';
import ExampleWorkModal from '../js/example-work-modal';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { isMainThread } from 'worker_threads';

const myExample = {
	'title': "Coding",
	'href': "http://example.com",
	'desc': "Lorum ipsum dolor sit amet, etc.",
	'image': {
		'desc': "example screenshot of a project involving code",
		'src': "images/example1.png",
		'comment': ""
	}
};

Enzyme.configure({adapter: new Adapter() });

describe("ExampleWorkModal", () => {
	let component = shallow(<ExampleWorkModal example={myExample} open={false}/>);
	let anchors = component.find("a");
	let openComponent = shallow(<ExampleWorkModal example={myExample} open={true}/>);

	it("Should contain a single a element", () => {
		expect(anchors.length).toEqual(1);
	});

	it("Should link to our project", () => {
		expect(anchors.prop('href')).toEqual(myExample.href);
	});

	it("Should have the modal class set correctly", () => {
		expect(component.find(".background--skyBlue").hasClass("modal--closed")).toBe(true);
		expect(openComponent.find(".background--skyBlue").hasClass("modal--open")).toBe(true);
	});
});