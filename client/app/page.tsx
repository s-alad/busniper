'use client';

import Image from 'next/image'
import styles from './page.module.css'
import Link from 'next/link';


export default function Home() {

	function register() {
		console.log("register")
	}

	function login() {
		let r = fetch('/api/login')
	}

	function index() {
		let r = fetch('/api/index')
	}

	return (
		<main className={styles.main}>
			<h1>
				EMPTYCLASS
			</h1>

			<form action="https://127.0.0.1:5000/login" method="GET">
				<input type="submit" value="Press to log in"/>
			</form>

			<button onClick={() => index()}>fetch</button>


			<Link href='http://127.0.0.1:5000/login'>Login</Link>

			<div>
				<input placeholder='College'></input>
				<input placeholder='Department'></input>
				<input placeholder='Course'></input>
				<input placeholder='Section'></input>
				<button>Submit</button>
			</div>
		</main>
	)
}
